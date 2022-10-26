"""
Test the auth module
"""
from datetime import datetime, timedelta

import jwt
import pytest

from auth import JWTProcessor


def test_auth_decode():
    """
    Test the auth token decoding process
    1) payload == decoded
    2) test the signature expiration
    """
    # 1) Test payload verification
    payload = {
        "email": "test@email.com",
        "user_id": 256,
        "exp": int((datetime.now() + timedelta(days=7)).timestamp())
    }
    
    token = JWTProcessor.encode(payload)
    decoded = JWTProcessor.decode(token)
    assert decoded == payload

    # 2) The signature must be expired and raise the Exception
    payload["exp"] = int((datetime.now() - timedelta(days=1)).timestamp())
    with pytest.raises(jwt.ExpiredSignatureError):
        JWTProcessor.decode(JWTProcessor.encode(payload))