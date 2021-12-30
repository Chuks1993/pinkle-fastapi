from fastapi import Depends
from ariadne import convert_kwargs_to_snake_case
from sqlalchemy.orm import Session
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import func

# from app.utils import query_to_dict
from ..models import Post, Vote, User, Comment
from ..database import SessionLocal


# https://github.com/tiangolo/fastapi/issues/1279


@convert_kwargs_to_snake_case
def resolve_posts(_, info: GraphQLResolveInfo, params):
    search = params.get("search", "")
    limit = params.get("limit")
    skip = params.get("skip")
    db = info.context["db"]
    results = (
        db.query(
            Post,
            func.count(Vote.post_id).label("votes"),
            func.count(Comment.post_id).label("comments"),
        )
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .join(Comment, Comment.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .filter(func.lower(Post.title).contains(search.lower()))
        .limit(limit)
        .offset(skip)
        .all()
    )
    db.close()
    posts = []
    # TODO: Find a better way to handle this
    # TODO: Truncate content on return
    for (
        post,
        votes,
        comments,
    ) in results:
        posts.append(
            {
                **post.__dict__,
                "votes": {"count": votes},
                "comments": {"count": comments},
            }
        )
    # print(posts)
    # print([dict(r) for r in results])
    if not results:
        return {"error": "Could not get the posts"}
    return {"result": posts}
    # return {"error": "hello"}


@convert_kwargs_to_snake_case
def resolve_create_post(_, info: GraphQLResolveInfo, params):
    auth: AuthJWT = info.context["auth"]
    auth.jwt_required()
    db: Session = info.context["db"]
    post = params
    current_user_id = auth.get_jwt_subject()
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        return {"error": "Cant validate user"}
    new_post = Post(author_id=current_user_id, **post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"result": new_post}


@convert_kwargs_to_snake_case
def resolve_post_by_id(_, info: GraphQLResolveInfo, params):
    db: Session = info.context["db"]
    postId = params
    res = (
        db.query(
            Post,
            func.count(Vote.post_id).label("votes"),
            func.count(Comment.post_id).label("comments"),
        )
        .filter(Post.id == postId)
        .group_by(Post.id)
        .first()
    )

    if not res:
        return {"error": f"Cant find post with id {postId}"}
    result = {
        **res[0].__dict__,
        "votes": {"count": res[1]},
        "comments": {"count": res[2]},
    }
    return {"result": result}
