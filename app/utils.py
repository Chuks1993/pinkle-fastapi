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


async def get_graphql_context(request: Request, db: Session) -> GraphQLContext:
    return {"request": request, "db": db}


async def resolve_graphql_context(request: Request) -> GraphQLContext:
    return await get_graphql_context(request, request["state"]["db"])
