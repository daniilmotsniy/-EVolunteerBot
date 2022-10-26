"""
Conftest for the order module only
"""

from asyncio import AbstractEventLoop
import pytest

from order.models import OrderDBModel
from user.models import UserDBModel


@pytest.fixture
def create_order(new_event_loop: AbstractEventLoop) -> OrderDBModel:
    """
    Create a single Order DB instance
    """
    order_instance: OrderDBModel = None
    def subfunction(user: UserDBModel):
        nonlocal order_instance
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

    new_event_loop.run_until_complete(order_instance.delete())
    