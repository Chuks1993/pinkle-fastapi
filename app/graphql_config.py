from ariadne.objects import MutationType
from fastapi import FastAPI
from ariadne import (
    QueryType,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.asgi import GraphQL

from app.utils import resolve_graphql_context
from .resolvers import post, user
from .scarlars import datetime_scalar


type_defs = [load_schema_from_path("app/schema.gql")]

query = QueryType()
mutation = MutationType()

# POST
query.set_field("posts", post.resolve_posts)
query.set_field("postById", post.resolve_post_by_id)
mutation.set_field("createPost", post.resolve_create_post)

# USER
mutation.set_field("createUser", user.resolve_create_user)
mutation.set_field("editUser", user.resolve_update_user)

app = FastAPI()

origins = ["http://localhost:3000"]


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    datetime_scalar,
    snake_case_fallback_resolvers,
)


# settings.debug should be used
graphql = GraphQL(schema, debug=True, context_value=resolve_graphql_context)
