import uvicorn
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, status, HTTPException, Response

from app.database import get_db
from starlette.datastructures import URL
from fastapi import Depends

from . import graphql_config
from .routers import auth

# TODO: Setup poetry
# TODO: Setup Redis
app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Very useful for letting me know whats going on This returns a json response and not an error which might alter functionality in client
# @app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    # return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    raise HTTPException(status_code=exc.status_code, detail=exc)


app.include_router(auth.router)


@app.get("/graphql")
async def graphiql(request: Request):
    request._url = URL("/graphql")
    return await graphql_config.graphql.render_playground(request=request)


# async def build_graphql_context(request: Request, authorization: str):
#     return tools.DictObject(
#         req=request,
#         authorization=authorization,
#     )

# @app.post("/graphql")
# async def graphql(request: Request, authorization: str = Header(None)):
#     request_data = dict(request)
#     ctx = await build_graphql_context(request, authorization)
#     success, response = await gql_app.execute(request, context=ctx)
#     return JSONResponse(content=response, status_code=200 if success else 400)


@app.post("/graphql")
async def graphql_post(
    request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    request.state.db = db
    request.state.auth = Authorize
    return await graphql_config.graphql.graphql_http_server(request=request)


def dev():
    """Launched with `poetry run dev` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
