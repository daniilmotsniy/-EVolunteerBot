"""
Test /api/order endpoints
"""

from typing import Callable


def test_get_order(access_token_func: Callable):
    """
    Test getting a single order
    """
    access_token_func = [""]
    