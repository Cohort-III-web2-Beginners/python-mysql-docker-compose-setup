from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(User):
    id: int
    created_at: datetime
    updated_at: datetime