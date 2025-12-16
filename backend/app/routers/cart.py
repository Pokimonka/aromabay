from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .users import get_current_user
from ..database import get_db
from .. import crud, schemas, models

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=schemas.CartResponse)
def add_to_cart(
        cart_item: schemas.CartItemCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
    user_id = current_user.id
    # Создаем заказ
    db_cart = crud.add_to_cart(db=db, user_id=user_id, item_data=cart_item)
    print(db_cart)

    return db_cart


@router.get("/", response_model=schemas.CartResponse)
def get_user_cart(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    print("get_cart")
    cart = crud.get_cart_items(db, user_id=current_user.id)

    return cart

@router.put("/{perfume_id}", response_model=schemas.CartResponse)
def update_quantity(
        perfume_id: int,
        cart_item: schemas.CartItemUpdate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    print("get_cart")
    cart = crud.update_perfume_quantity(db,
                                        user_id=current_user.id,
                                        perfume_id=perfume_id,
                                        quantity=cart_item.quantity)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

@router.delete("/{perfume_id}", response_model=schemas.CartResponse)
def delete_item(
        perfume_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    cart = crud.remove_item_from_cart(db,
                                user_id=current_user.id,
                                perfume_id=perfume_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

@router.delete("/", response_model=schemas.CartResponse)
def delete_all_after_order(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    cart = crud.remove_from_cart(db,
                                user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart
