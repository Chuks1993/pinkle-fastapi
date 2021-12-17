from typing import Dict
from ariadne import convert_kwargs_to_snake_case
from graphql.type import GraphQLResolveInfo

from ..models import User
from .. import utils
from ..oauth2 import create_access_token, get_current_user


@convert_kwargs_to_snake_case
def resolve_get_token(_, info: GraphQLResolveInfo, user_credentials):
    db = info.context["db"]
    user = db.query(User).filter(User.email == user_credentials["email"]).first()
    if not user or not utils.verify(user_credentials["password"], user.password):
        return {"message": "Invalid Credentials"}
    access_token = create_access_token(data={"user_id": user.id})
    return {"token": {"access_token": access_token, "token_type": "bearer"}}


@convert_kwargs_to_snake_case
def resolve_create_user(_, info: GraphQLResolveInfo, user):
    db = info.context["db"]
    hashed_password = utils.hash(user["password"])
    user["password"] = hashed_password
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": new_user}


# TODO: turn getting user into a decorator and make sure it checks for Bearer
@convert_kwargs_to_snake_case
def resolve_me(_, info: GraphQLResolveInfo):
    db = info.context["db"]
    token = info.context.get("request").headers.get("authorization")
    if not token:
        return {"error": "User not authenticated"}
    current_user = get_current_user(token, db)
    if not current_user:
        return {"error": "Couldnt get user based on that"}
    return {"me": current_user}


# @convert_kwargs_to_snake_case
# def resolve_log_out(_, info: GraphQLResolveInfo):
#     print("signing out")
