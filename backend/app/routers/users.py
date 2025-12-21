import json

from fastapi import APIRouter, Depends, Request, HTTPException, Response

from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.database import get_db
from app.session_manager import get_user_id_from_session, create_session, delete_session

router = APIRouter(prefix="/auth", tags=["register"])

def get_user_by_id(db: Session, user_id: int) -> models.User:
    user_info = (db.
               query(models.User).
               filter(models.User.id==user_id,).
               first()
               )
    if user_info:
        return user_info
    return None

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")
    print(f"token from get_current_user: {token}")
    user_id = get_user_id_from_session(db, token)
    print(f"current user: {user_id}")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not auth")
    user_info = get_user_by_id(db, user_id)
    return user_info

@router.post("/register", response_model=schemas.AuthResponse)
def create_user(
        user: schemas.UserRegister,
        response: Response,
        db: Session = Depends(get_db)):
    user_by_username, user_by_email = crud.get_user_by_email_or_us(db, user.username, user.email)
    if user_by_username and user_by_email:
        raise HTTPException(status_code=400, detail="Username and email already exists")
    if user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = crud.create_user(db, user)
    print(f"dp_user {db_user}")
    token = create_session(db, db_user.id)
    print(f"token {token}")

    user = schemas.AuthResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        telegram_username=db_user.telegram_username,
        session_token=token,
        message="success"
    )
    print(f"user {user}")
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=7*24*60*60,
        secure=False,
        samesite="lax"
    )

    return user

@router.get("/me", response_model=schemas.UserResponse)
def get_user(
    current_user: models.User = Depends(get_current_user)):
    print(f"/me current_user: {current_user}")
    user = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "telegram_username": current_user.telegram_username,
        "role": current_user.role
    }

    return user

@router.post("/login", response_model=schemas.AuthResponse)
def login(
        user: schemas.UserLogin,
        response: Response,
        db: Session = Depends(get_db)):

    print(f"login: {user.email}")
    existing_user = crud.get_user_by_email_or_us(db, '', user.email)

    if not existing_user or not crud.verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong username or password")

    token = create_session(db, existing_user.id)
    print(f"token: {token}")
    user = schemas.AuthResponse(
        id=existing_user.id,
        username=existing_user.username,
        email=existing_user.email,
        telegram_username=existing_user.telegram_username,
        session_token=token,
        message="success"
    )

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=7*24*60*60,
        secure=False,
        samesite="lax"
    )

    return user

@router.post("/logout", response_model=None)
def logout(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)):

    token = request.cookies.get("session_token")
    print(f"logout_token {token}")
    if token:
        delete_session(db, token)
        response.delete_cookie("session_token")

    return {"message": "success"}
