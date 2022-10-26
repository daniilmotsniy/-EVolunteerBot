"""
Core application exceptions
"""

from typing import Any, Dict, Optional
from fastapi.exceptions import HTTPException


class InvalidCredentialsException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=401, detail=detail or "Invalid credentials")
        self.headers = headers
      