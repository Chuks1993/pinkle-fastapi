from typing import Dict
from ariadne import convert_kwargs_to_snake_case
from fastapi_jwt_auth.auth_jwt import AuthJWT
from graphql.type import GraphQLResolveInfo
from sqlalchemy.orm.session import Session

from .models import User
from ..shared import utils


@convert_kwargs_to_snake_case
def resolve_create_user(_, info: GraphQLResolveInfo, params):
    db = info.context["db"]
    user = params
    q = db.query(User.id).filter(User.email == user["email"])
    if q.first():
        return {"error": "This email is already in use"}
    hashed_password = utils.hash(user["password"])
    user["password"] = hashed_password
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"result": new_user}


@convert_kwargs_to_snake_case
def resolve_update_user(_, info: GraphQLResolveInfo, params):
    auth: AuthJWT = info.context["auth"]
    auth.jwt_required()
    db: Session = info.context["db"]
    user = params
    hashed_password = utils.hash(user["password"])
    user["password"] = hashed_password
    updated_user = User(**user)
    db.add(updated_user)
    db.commit()
    db.refresh(updated_user)
    return {"result": updated_user}
