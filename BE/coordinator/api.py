"""
Coordinator app API endpoints
"""
from typing import List, Optional

from fastapi import APIRouter, Depends

from auth.dependencies import token_user
from coordinator.models import BucketDBModel
from order.constants import ORDER_STATUS_NEW
from order.models import OrderDBModel
from user.models import UserDBModel

router = APIRouter()


@router.get(
    "/coordinator",
    summary="Get a list of coordinators with its orders",
    response_description="List coordinators with its orders",
)
async def get_coordinator(
    status: Optional[int] = None,
    sort: Optional[str] = None,
    coordinator: Optional[str] = None,
    token_user: UserDBModel = Depends(token_user),
) -> List[BucketDBModel]:
    """
    Orders from DB with filter and sort

    :param operator: this is email of user who makes order_2_pdf
    :param status: Optional[int]: order_2_pdf's status
    :param sort: Optional['desc', 'asc']: sort orders by date
    :param coordinator: Optional[str]: coordinator's name
    :rtype: List[BucketDBModel]
    :return:
    """
    coordinators = await BucketDBModel.get_coordinators()
    
    operator_id = token_user.id if token_user.is_operator() else None
    # operator_id = token_user.id if token_user.is_operator() else None

    if token_user.is_operator() and status != ORDER_STATUS_NEW:
        for coord in coordinators:
            coord["orders"] = list(filter(
                lambda order: order.get("operator_id") == operator_id,
                coord["orders"]
            ))

    if coordinator:
        coordinators = list(filter(
            lambda el: el["coordinator"] == coordinator,
            coordinators
        ))

    if status:
        for coord in coordinators:
            coord["orders"] = [
                order for order in coord["orders"]
                if order["status"] == status
            ]

    if sort:
        reverse = {"asc": False, "desc": True}
        for coord in coordinators:
            coord["orders"].sort(
                key=lambda i: i["date"],
                reverse=reverse.get(sort, True),
            )

    coordinator_list = list(filter(lambda el: el.get("orders"), coordinators))
    return coordinator_list



