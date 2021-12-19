from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT


from .. import database, models, utils, config
from . import schemas

router = APIRouter(tags=["Authentication"])


@AuthJWT.load_config
def get_config():
    return config.settings


@router.post("/login", response_model=schemas.AuthResponse)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
    Authorize: AuthJWT = Depends(),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    # IMPORTANT: We use db user to create token and NOT user passed in from input
    access_token = Authorize.create_access_token(
        subject=user.id, fresh=True, expires_time=timedelta(seconds=2)
    )
    refresh_token = Authorize.create_refresh_token(subject=user.id)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg": "successfully logged in"}


# TODO: make user require a fresh token for account or sensitive data meaning they need to log back in


@router.post("/refresh", response_model=schemas.AuthResponse)
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    # TODO: maybe check if this user exists before still authing them
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(
        subject=current_user, fresh=False, expires_time=timedelta(seconds=2)
    )
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "successfully logged in"}


@router.delete("/logout", response_model=schemas.AuthResponse)
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logged out"}


@router.get(
    "/me",
    # TODO: update the schema out for this query it causes a CORS issue on the front end idk why but yeah -_-
    response_model=schemas.UserOut,
)
def get_me(Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    Authorize.jwt_required()

    current_user_id = Authorize.get_jwt_subject()
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    # TODO: have to return a dict or the response basically dissappearce on client
    if not user:
        # TODO: should raise error here and prevent the code from returning
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )
        # TODO: I definetly shouldnt and dont want to parse through the dict manually
    return {"id": user.id, "email": user.email, "createdAt": user.created_at}


# TODO: Dont see the point of this but adding it for refrence
# @router.post('/fresh-login')
# def fresh_login(user: User, Authorize: AuthJWT = Depends()):
#     """
#     Fresh login endpoint. This is designed to be used if we need to
#     make a fresh token for a user (by verifying they have the
#     correct username and password). Unlike the standard login endpoint,
#     this will only return a new access token, so that we don't keep
#     generating new refresh tokens, which entirely defeats their point.
#     """
#     if user.username != "test" or user.password != "test":
#         raise HTTPException(status_code=401,detail="Bad username or password")

#     new_access_token = Authorize.create_access_token(subject=user.username,fresh=True)
#     return {"access_token": new_access_token}
