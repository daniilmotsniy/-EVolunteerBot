
from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, Field
from database import db
from order.models import OrderDBModel


class BucketDBModel(BaseModel):
    name: str = Field(...)
    orders: list[OrderDBModel]
    q_name: str = Field(...)
    q_city: str = Field(...)

    @staticmethod
    async def get_coordinators(query=None) -> list:
        coordinators = list()
        try:
            for row in await db.aiogram_bucket.find(query).to_list(1000):
                coordinator = {
                    "coordinators": row["bucket"]["name"],
                    "orders": row["bucket"]["orders"],
                }
                coordinators.append(coordinator)
        except Exception:
            raise HTTPException(status_code=401, detail="Bad request")

        return coordinators

    @staticmethod
    async def update_coordinator(filter=None, update=None):
        update_result = await db["aiogram_bucket"].update_one(filter, update)


class AiogramBucketDBModel(BaseModel):
    user: int = Field(...)
    chat: int = Field(...)
    bucket: BucketDBModel = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
