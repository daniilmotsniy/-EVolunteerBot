"""
User app API endpoints
"""
from fastapi import Depends, HTTPException, Request, APIRouter

from auth.decorators import roles_required
from auth.dependencies import token_user
from auth.models import AccessTokenAPIModel, RefreshTokenAPIModel, UserCredentials
from core.exception import InvalidCredentialsException
from user.models import UserAPIModel, UserDBModel

router = APIRouter()



@router.get("/user/self")
async def get_user(
    request: Request,
    token_user: UserDBModel = Depends(token_user),
) -> UserAPIModel:
    """Get the user by the token supplied"""
    user: UserDBModel = await UserDBModel.get(pk=token_user.id)
    return UserAPIModel(**user.dict())


@router.get("/user/{user_id}")
@roles_required(("admin", "operator"))
async def get_user(
    request: Request,
    user_id: str,
    token_user: UserDBModel = Depends(token_user),
) -> UserAPIModel:
    """Get a single User"""
    user: UserDBModel = await UserDBModel.get(pk=user_id)
    # Can't get restricted user
    if not token_user.is_admin() and user.id != token_user.id:
        raise InvalidCredentialsException()
    return user


@router.post("/auth/login")
async def login(credentials: UserCredentials) -> RefreshTokenAPIModel:
    """
    Log in the user with the credentials
    """
    try:
        user: UserDBModel = await UserDBModel.get(email=credentials.email)
        refresh_token = user.login(credentials.password)
        return refresh_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/auth/refresh/{refresh}")
async def refresh(refresh: str) -> AccessTokenAPIModel:
    """
    Obtain a new access token by providing the refresh token
    :param refresh: str: The refresh token to get an access token upon
    """
    try:
        return await UserDBModel.refresh_token(refresh)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token data")
