"""
Server codebase entrypoint
"""

from coordinator.api import router as coordinator_router
from server import app
from user.api import router as user_router
from order.api import router as order_router


@app.get("/", response_description="Hello")
async def welcome():
    """Test entrypint"""
    return 'Welcome to our server!'


app.include_router(user_router, tags=["Auth User"], prefix="/api")
app.include_router(coordinator_router, tags=["Coordinator"], prefix="/api")
app.include_router(order_router, tags=["Order"], prefix="/api")
