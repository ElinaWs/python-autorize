from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"


class UserLoginSchema(BaseModel):
    login: str
    password: str


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True