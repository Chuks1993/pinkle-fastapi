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
    current_user_id = auth.get_jwt_subject()
    user_query = db.query(User).filter(User.id == params["id"])
    user = user_query.first()
    if user == None:
        return {"error": f"Unable to find user with id: {params['id']}"}
    if user.id != current_user_id:
        return {"error": "Not authroized to perform this request"}
    user_query.update(params["data"], synchronize_session=False)
    db.commit()
    return {"result": user}
