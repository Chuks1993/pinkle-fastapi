from fastapi import Depends
from ariadne import convert_kwargs_to_snake_case
from sqlalchemy.orm import Session
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from typing import List, Optional

from sqlalchemy import func
from starlette.requests import cookie_parser
from ..models import Post, Vote
from ..database import SessionLocal


# https://github.com/tiangolo/fastapi/issues/1279


@convert_kwargs_to_snake_case
def resolve_posts(_, info: GraphQLResolveInfo):
    db = info.context["db"]
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .all()
    )
    db.close()
    return posts


@convert_kwargs_to_snake_case
def resolve_create_post(self, info):
    return "hello"
