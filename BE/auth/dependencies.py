from fastapi import HTTPException, Header

from .auth import JWTProcessor

from user.models import UserDBModel


async def token_user(x_auth_token: str = Header(...)) -> UserDBModel:
    """
    Dependency with missions:
    1) check if `X-Auth-Token` is supplied and its data is correct
    2) retrieve the UserDBModel with data supplied
    :return UserDBModel: The user data from dict
    """
    splitted = x_auth_token.split()
    if len(splitted) != 2:
        raise HTTPException(status_code=400, detail="X-Auth-Token invalid format")
    token = splitted[1]
    try:
        token_data = JWTProcessor.decode(token)
        user = await UserDBModel.get(token_data["id"]) 
        return user
    except Exception:
        raise HTTPException(status_code=401, detail=f"Token is invalid or expired")
