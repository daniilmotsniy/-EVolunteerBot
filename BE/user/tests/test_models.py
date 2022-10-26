"""
Test User models
"""
from asyncio import AbstractEventLoop, get_event_loop, new_event_loop

import pytest

from user.models import UserDBModel


def test_user_create(new_event_loop: AbstractEventLoop):
    """
    Test user DB creation
    """
    async def test_user_create_async():
        payload = {
            "email": "test@email.com",
            "password": "simple_pass123",
        }
        db_user = await UserDBModel.create(payload)
        # Find user by PK (ID | UUID)
        user_found: UserDBModel = await UserDBModel.get(db_user.id)
        assert len(user_found.password) == 56
        assert user_found.password != payload["password"]
        assert user_found.email == payload["email"]

        # Find user by email
        user_found: UserDBModel = await UserDBModel.get(email=user_found.email)
        assert user_found.email == payload["email"]

        # Test password
        assert user_found.password_matches(payload["password"]) is True
        assert user_found.password_matches(payload["password"].upper()) is False

        users_deleted = await UserDBModel.delete_all({"email": "test@email.com"})
        assert users_deleted == 1
    new_event_loop.run_until_complete(test_user_create_async())