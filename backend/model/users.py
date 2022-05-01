"""user module"""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    """Login Schema"""
    username: str
    password: str
    class Config:
        """Pydantic config"""
        schema_extra = {
            'examples': [
                {
                    'username': 'John_Doe_123',
                    'password': 'password123',
                }
            ]
        }


class UserSchema(BaseModel):
    """User Schema"""
    name: str
    age: int
    address: str
    email: EmailStr
    phone: int
    username: str
    password: str
    role:str
    created_at : Optional[datetime] = datetime.now(timezone.utc)
    class Config:
        """Pydantic config"""
        schema_extra = {
            'examples': [
                {
                    'name': 'John Doe',
                    'age': 25,
                    'address': '123 Main St',
                    'email': 'Jhon.Doe@missing.com',
                    'phone': 1234567890,
                    'username': 'John_Doe_123',
                    'password': 'password123',
                    'role':'admin',
                    'created_at': datetime.now(timezone.utc),
                }
            ]
        }
