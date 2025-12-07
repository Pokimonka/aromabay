import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import models

def create_session(db: Session, user_id: int):
    token = secrets.token_urlsafe(32)

    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    session = models.UserSession(user_id=user_id, session_token=token, expires_at=expires_at)
    print(f"Создаем сессию для юзера {user_id} с токеном: {token}")
    db.add(session)
    db.commit()

    return token

def get_user_id_from_session(db: Session, token: str):
    if not token:
        return None

    session = (db.
               query(models.UserSession).
               filter(models.UserSession.session_token==token,
                     models.UserSession.expires_at > datetime.now(timezone.utc)).
               first()
               )
    if session:
        print("Такая сессия есть!")
        return session.user_id

    return None

def delete_session(db: Session, token: str):
    session = (db.
               query(models.UserSession).
               filter(models.UserSession.session_token == token).
               first()
               )

    if session:
        db.delete(session)
        db.commit()

