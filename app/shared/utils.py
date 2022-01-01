from fastapi_jwt_auth.auth_jwt import AuthJWT
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.requests import Request

from typing import Any, Dict


GraphQLContext = Dict[str, Any]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_graphql_context(
    request: Request, db: Session, auth: AuthJWT
) -> GraphQLContext:
    return {"request": request, "db": db, "auth": auth}


async def resolve_graphql_context(request: Request) -> GraphQLContext:
    return await get_graphql_context(
        request, request["state"]["db"], request["state"]["auth"]
    )
