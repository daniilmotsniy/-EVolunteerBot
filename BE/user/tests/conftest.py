"""
Conftest
"""
from typing import List
import pytest
from asyncio import AbstractEventLoop

from user.models import UserDBModel


@pytest.fixture
def delete_test_users(new_event_loop: AbstractEventLoop):
    async def async_delete():
        return await UserDBModel.delete_all({"email": "test@email.com"})
    return lambda: new_event_loop.run_until_complete(async_delete())
