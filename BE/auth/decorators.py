"""
Decorators
"""

from functools import wraps
from typing import Any, Iterable, Optional

from fastapi import HTTPException

from user.models import UserDBModel


def roles_required(roles: Optional[Iterable] = None) -> Any:
  """
  Decorator to check if user is in roles.
  The check is handled with `token_user` parameter
  :param Optional[Iterable] roles: List of roles to allow access to. If None, no check is going 
  :rtype: Any
  """
  def function(original_function):
    """Function to return"""
    @wraps(original_function)
    async def main_callable(*args, **kwargs):
      """Main callable to substitute by"""
      user: UserDBModel = kwargs.get("token_user")
      has_intersection = any(user_role in roles for user_role in user.roles)
      if not has_intersection:
        raise HTTPException(status_code=401, detail="Invalid role")
      result = await original_function(*args, **kwargs)
      return result
    return main_callable
    
  return function