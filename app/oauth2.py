from fastapi.param_functions import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    # TODO: improve exceptions
    try:
        token_data = token.split()
        if token_data[0] is not "Bearer":
            return {"error": "Invalid credentials"}
        # TODO: Not sure if this is the best way and we may need to raise errors
        payload = jwt.decode(token_data[1], SECRET_KEY, algorithms=ALGORITHM)
        id: str = str(payload.get("user_id"))
        if id is None:
            return {"error": "Could not validate credentials"}
    except JWTError:
        return {"error": "Invalid token"}

    return {"id": id}


def get_current_user(token, db: Session):
    token = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == token["id"]).first()
    return user.__dict__
