
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field


class UserDocument(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
