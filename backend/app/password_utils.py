from fastapi.security import OAuth2PasswordBearer
# from passlib.context import CryptContext
import bcrypt

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(plain_password: str) -> bytes:
    # return pwd_context.hash(plain_password)
    return bcrypt.hashpw(
        bytes(plain_password, encoding="utf-8"),
        bcrypt.gensalt(),
    )

def verify_password(plain_password:str, hashed_password: str) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        bytes(hashed_password.encode('utf-8')),
    )
