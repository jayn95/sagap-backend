# from pydantic import BaseModel

# class UserAuth(BaseModel):
#     username: str
#     password: str

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str
    eid: str | None = None


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    eid: str | None
    status: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str