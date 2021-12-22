from typing import Dict
from ariadne import convert_kwargs_to_snake_case
from graphql.type import GraphQLResolveInfo

from ..models import User
from .. import utils


@convert_kwargs_to_snake_case
def resolve_create_user(_, info: GraphQLResolveInfo, params):
    # TODO: check if user already exists
    db = info.context["db"]
    user = params
    hashed_password = utils.hash(user["password"])
    user["password"] = hashed_password
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"result": new_user}
