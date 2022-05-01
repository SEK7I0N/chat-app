"""message module"""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel


class MessageSchema(BaseModel):
    """Message Schema"""
    sender: str
    group: str
    content :str
    created_at : Optional[datetime] = datetime.now(timezone.utc)
    sender_id: Optional[int] = -1
    group_id: Optional[int] = -1
    class Config:
        """Pydantic config"""
        schema_extra = {
            'examples': [
                {
                    'sender': 'John_Doe_123',
                    'chat_room': 'Python Tutorial',
                    'message_content': 'These are the Message contents 📩🐣🔥',
                    'created_at': datetime.now(timezone.utc),
                }
            ]
        }
