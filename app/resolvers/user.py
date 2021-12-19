from typing import Dict
from ariadne import convert_kwargs_to_snake_case
from graphql.type import GraphQLResolveInfo

from ..models import User
from .. import utils


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
