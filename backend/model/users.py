"""user module"""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel


class LoginDetails(BaseModel):
    """Login details"""
    username: str
    password: str

class UserDetails(BaseModel):
    """Login details"""
    id : int
    name: str
    age: int
    address: str
    email: str
    phone: int
    username: str
    password: str
    created_timestamp : Optional[datetime] = datetime.now(timezone.utc)
