"""
Authentication-related classes:
1) PasswordManager
2) JWTProcessor
"""

from hashlib import sha224
import jwt

from config import settings


class JWTProcessor:
    """
    Class to handle JWT methods
    """

    @classmethod
    def encode(cls, payload: dict) -> str:
        """
        :param dict payload: data to be encoded into the token
        :rtype: str
        """
        return jwt.encode(payload, key=settings.AUTH_JWT_PRIVATE_KEY, algorithm=settings.AUTH_JWT_ALGORITHM)

    @classmethod
    def decode(cls, token: dict) -> dict:
        """
        :param str token: the Access/Refresh/Any token
        :raises jwt.ExpiredSignatureError: the signature is expired
        :rtype: dict
        """
        return jwt.decode(token, key=settings.AUTH_JWT_PRIVATE_KEY, algorithms=(settings.AUTH_JWT_ALGORITHM,))


class PasswordManager:
    """
    The class to work with password hashes
    """

    @staticmethod
    def hash(password: str) -> str:
        """
        Hash the password
        """
        hash_cycles = settings.AUTH_PASSWORD_HASH_CYCLES
        hashed: str = password

        for _ in range(hash_cycles):
            hashed = hashed + settings.AUTH_PASSWORD_HASH_SALT
            hashed = sha224(hashed.encode("utf-8")).hexdigest()
        return hashed
