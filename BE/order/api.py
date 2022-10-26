"""
Coordinator app API endpoints
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from auth.dependencies import token_user
from coordinator.models import BucketDBModel
from core.exception import InvalidCredentialsException
from database.database import db
from order.models import OrderDBModel, UpdateStatusOrderAPIModel
from order.pdf_upload_manager import get_pdf_url_for_orders
from user.models import UserDBModel
from util.constants import ADMIN_ROLE

router = APIRouter()


@router.get(
    "/order/{order_id}}",
    summary="Get the Order by its ID",
    response_description="List coordinators with its orders",
)
async def get_order(
    order_id: int,
    token_user: UserDBModel = Depends(token_user),
) -> OrderDBModel:
    """
    Orders from DB with filter and sort

    :param int order_id: Id of the order to get
    :rtype: OrderDBModel
    :return: The order
    """
    order = await OrderDBModel.get(order_id)
    return order


@router.patch(
    "/order/{order_id}",
    response_description="Update the Order status",
)
async def update_order_status(
        order_id: str,
        status_model: UpdateStatusOrderAPIModel,
        token_user: UserDBModel = Depends(token_user),
):
    """
    The resource to update the order status
    """
    try:
        coordinator_id = int(order_id.split(".")[0])
    except Exception:
        raise HTTPException(status_code=404, detail=f"Bad order_id")
    
    operator_data = {
        "id": token_user.id,
        "fullname": token_user.fullname,
    }
    if status_model.status == OrderDBModel.STATUS_NEW:
        # If "new" is the status to update to
        operator_data = {}

    update_result = await BucketDBModel.update_coordinator(
        {
            "bucket.orders.order_id": order_id, "user": coordinator_id
        },
        {
            "$set": {
                "bucket.orders.$.status": status_model.status,
                "bucket.orders.$.operator": operator_data.get("fullname"),
                "bucket.orders.$.operator_id": operator_data.get("id")
            }
        },
    )

    coordinators = await BucketDBModel.get_coordinators({"user": coordinator_id})

    for coordinator in coordinators:
        coordinator["orders"] = [
            order for order in coordinator["orders"] if order["order_id"] == order_id
        ]

    return coordinators


@router.delete(
    "/order/{order_id}",
    response_description="Delete the Order",
)
async def delete_order(
    order_id: str,
    token_user: UserDBModel = Depends(token_user),
):
    try:
        user_id = int(order_id.split(".")[0])
    except Exception:
        raise HTTPException(status_code=404, detail=f"Bad order_id")

    del_status = 4
    update_result = await BucketDBModel.update_coordinator(
        {"bucket.orders.order_id": order_id, "user": user_id},
        {"$set": {"bucket.orders.$.status": del_status}},
    )

    coordinators = await BucketDBModel.get_coordinators({"user": user_id})

    for coordinator in coordinators:
        coordinator["orders"] = [
            order for order in coordinator["orders"] if order["order_id"] == order_id
        ]

    return coordinators


@router.get(
    "/order/pdf",
    response_description="Link for download new orders as PDF",
)
async def create_pdf(
    token_user: UserDBModel = Depends(token_user),
):
    """
    Create a PDF file report based on the Order
    """
    if not token_user.is_admin():
        raise InvalidCredentialsException()

    users = await db["aiogram_bucket"].find({'bucket.orders.status': 1}).to_list(1000)

    new_orders = (order for user in users for order in user['bucket']['orders'] if order['status'] == OrderDBModel.STATUS_NEW)

    return get_pdf_url_for_orders(new_orders)
