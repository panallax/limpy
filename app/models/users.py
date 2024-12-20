from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str
    access: bool
    withdrawals: list[str] = []

class UserAuth(BaseModel):
    username: str
    access: bool

class UserResponse(BaseModel):
    id: str
    user_id: str
    name: str
    email: str
    access: bool
    withdrawals: list[str] = []
