import datetime
from typing import ClassVar

from pydantic import BaseModel, Field

from database.database import db


class UpdateStatusOrderAPIModel(BaseModel):
    status: int = Field(...)


class OrderDBModel(BaseModel):
    STATUS_NEW: ClassVar[int] = 1

    city: str = Field(...)
    name: str = Field(...)
    phone: str = Field(...)
    address: str = Field(...)
    people: int = Field(...)
    can_cook: bool = Field(...)
    food: str = None
    meds: str = None
    latitude: float = None
    longitude: float = None
    order_id: str = Field(...)
    status: int = Field(...)
    comment: str = None
    date: datetime.datetime = Field(...)
    operator: str = None

    @staticmethod
    async def get(pk: int):
        """
        Get the order by its ID (PK)
        """
        
        conditions = {"id": pk}
        result = await db.user.find_one(conditions)
        if result is None:
            return
        inst = OrderDBModel(**result)
        return inst

    async def delete(self):
        """
        Delete the order
        """
        if not self.order_id:
            raise Exception("The order does not exist")
        result = await db.order.delete_one({"id": self.order_id})
        if result.deleted_count != 1:
            raise Exception("The order is not deleted from the database")
