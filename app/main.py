from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_db
from starlette.datastructures import URL
from fastapi import Depends

from . import graphql_config
from .routers import auth

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/graphql")
async def graphiql(request: Request):
    request._url = URL("/graphql")
    return await graphql_config.graphql.render_playground(request=request)


# TODO: use cookie for refresh token


@app.post("/graphql")
async def graphql_post(request: Request, db: Session = Depends(get_db)):
    request.state.db = db
    return await graphql_config.graphql.graphql_http_server(request=request)
