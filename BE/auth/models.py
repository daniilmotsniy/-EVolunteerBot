"""
Authentication models
"""
from pydantic import BaseModel, Field


class RefreshTokenAPIModel(BaseModel):
    refresh: str = Field(...)
    exp: int = Field(...)


class AccessTokenAPIModel(BaseModel):
    token: str = Field(...)
    exp: int = Field(...)


class UserCredentials(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
