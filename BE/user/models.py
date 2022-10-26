"""
User DB / Pydantic model
"""
from typing import Optional
import uuid
from copy import copy
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, ValidationError

from auth import PasswordManager
from auth.auth import JWTProcessor
from auth.models import AccessTokenAPIModel, RefreshTokenAPIModel
from database import db


class UserAPIModel(BaseModel):
    """User API model"""
    id: str = ""
    email: str = Field(...)
    fullname: Optional[str] = Field(default=None)
    roles: list = Field(default_factory=list)
    created: datetime = Field(default_factory=lambda: datetime.now())


class UserDBModel(BaseModel):
    """User DB model"""
    id: str = ""
    email: str = Field(...)
    fullname: Optional[str] = Field(default=None)
    password: str = Field(..., min_length=56, max_length=56, repr=False)
    roles: list = Field(default_factory=list)
    created: datetime = Field(default_factory=lambda: datetime.now())

    @staticmethod
    async def create(payload: dict) -> "UserDBModel":
        """
        Validate, hash user's password, create the User
        """
        if await UserDBModel.get(email=payload["email"]):
            raise Exception("User already exists")
        safe_payload = copy(payload)
        safe_payload["password"] = PasswordManager.hash(safe_payload["password"])
        safe_payload["id"] = str(uuid.uuid4())
        
        inst = UserDBModel(**safe_payload)
        result = await db.user.insert_one(inst.dict())
        return inst

    @staticmethod
    async def get(pk: Optional[str] = None, email: Optional[str] = None) -> "UserDBModel":
        """
        Get the User by it's ID
        """
        conditions = {}
        if pk:
            conditions["id"] = pk
        if email:
            conditions["email"] = email
        result = await db.user.find_one(conditions)
        if result is None:
            return
        inst = UserDBModel(**result)
        return inst

    async def delete(self):
        """
        Delete the User
        """
        if not self.id:
            raise ValidationError("The user does not exist")
        result = await db.user.delete_one({"id": self.id})
        if result.deleted_count != 1:
            raise Exception("The user is not deleted from the database")

    @staticmethod
    async def delete_all(conditions: dict = None) -> int:
        """
        Delete all the User instances
        :return int: number of users deleted
        """
        if not conditions:
            conditions = {}
        result = await db.user.delete_many(conditions)
        return result.deleted_count

    def password_matches(self, password: str) -> bool:
        """
        Check if the raw password matches the User's password
        """
        return PasswordManager.hash(password) == self.password

    def login(self, password: str) -> RefreshTokenAPIModel:
        """
        Log In: Obtain a refresh token
        :param password: str: password to match this user with
        """
        if not self.id:
            raise ValidationError("The user does not exist")
        
        if not self.password_matches(password):
            raise ValidationError("The password is invalid")
        payload = {
            "id": self.id,
            "exp": int((datetime.now() + timedelta(days=7)).timestamp())
        }
        refresh = JWTProcessor.encode(payload)
        refresh_token = RefreshTokenAPIModel(
            refresh=refresh,
            exp=payload["exp"]
        )
        return refresh_token

    @staticmethod
    async def refresh_token(refresh_token: str) -> AccessTokenAPIModel:
        """
        Obtain an access token based on the RefreshToken
        """
        refresh_data = JWTProcessor.decode(refresh_token)
        _id = refresh_data["id"]
        if not _id:
            raise ValidationError("The id is empty")
        try:
            user = await UserDBModel.get(pk=_id)
        except Exception:
            raise ValidationError("The user does not exist")

        payload = {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname,
            "roles": user.roles,
            "exp": int((datetime.now() + timedelta(seconds=7)).timestamp())
        }
        token = JWTProcessor.encode(payload)
        access_token = AccessTokenAPIModel(
            token=token,
            exp=payload["exp"]
        )
        return access_token

    def is_admin(self) -> bool:
        return "admin" in self.roles

    def is_operator(self) -> bool:
        return "operator" in self.roles