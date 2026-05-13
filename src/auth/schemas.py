from datetime import datetime

from pydantic import BaseModel, model_validator


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    password_2: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_2:
            raise ValueError('Passwords do not match')
        return self

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
