from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel


class GroupSchema(BaseModel):
    """GroupSchema model"""
    name: str
    user: str
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    user_id: Optional[int] = -1
    group_id: Optional[int] = -1

    class Config:
        """Pydantic config"""
        schema_extra = {
            'examples': [
                {
                    'name': 'Group Name',
                    'created_at': datetime.now(timezone.utc),
                }
            ]
        }
