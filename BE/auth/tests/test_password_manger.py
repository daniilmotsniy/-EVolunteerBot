"""
Test the auth PasswordManager
"""
import pytest

from auth import PasswordManager
from config import settings


def test_password_manager_hashing():
    """
    Test the password manager hashing
    """
    # 1) Test hashing works consistently
    password = "rAnDoM_PaSsW0Rd2022"
    hashed = PasswordManager.hash(password)
    assert len(hashed) == 56
    rehashed = PasswordManager.hash(password)
    assert rehashed == hashed

    # 2) Change the cycles numberz
    settings.AUTH_PASSWORD_HASH_CYCLES -= 1
    rehashed = PasswordManager.hash(password)
    assert len(rehashed) == 56
    assert rehashed != hashed

    # 3) Replace the salt
    settings.AUTH_PASSWORD_HASH_SALT = "Random"
    rehashed = PasswordManager.hash(password)
    assert len(rehashed) == 56
    assert rehashed != hashed
