"""
General pytest dependency injection functions
"""

import asyncio
from asyncio import AbstractEventLoop
from typing import List

import pytest
from auth.models import AccessTokenAPIModel, RefreshTokenAPIModel

from database import db
from user.models import UserDBModel


@pytest.fixture
def event_loop():
    loop = getattr(event_loop, "loop", None)
    loop = loop or asyncio.get_event_loop()
    setattr(event_loop, "loop", loop)

    db.get_io_loop = asyncio.get_running_loop
    yield loop


@pytest.fixture
def new_event_loop():
    """
    Create and yield a new event loop
    """
    loop = asyncio.new_event_loop()
    db.get_io_loop = asyncio.get_running_loop
    yield loop


@pytest.fixture
def create_user_function(new_event_loop: AbstractEventLoop):
    """
    Create a DB User insance
    """
    db_user = None
    def subfunction(email=None, password=None, roles: List[str] = None):
        nonlocal db_user
        async def async_create():
            payload = {
                "email": email or "test@email.com",
                "password": password or "simple_pass123",
                "roles": roles or list(),
            }
            db_user: UserDBModel = await UserDBModel.create(payload)
            return db_user
        db_user = new_event_loop.run_until_complete(async_create())
        return db_user

    yield subfunction

    new_event_loop.run_until_complete(db_user.delete())


@pytest.fixture
def access_token_func(
    create_user_function: UserDBModel,
    new_event_loop: AbstractEventLoop
) -> AccessTokenAPIModel:
    """
    Generated user token
    """
    def func(*user_create_args, **user_create_kwargs):
        user = create_user_function(
            *user_create_args, **user_create_kwargs
        )
        refresh_token: RefreshTokenAPIModel = user.login("simple_pass123")
        access_token: AccessTokenAPIModel = new_event_loop.run_until_complete(
            UserDBModel.refresh_token(refresh_token.refresh)
        )
        return (access_token, user)
    return func