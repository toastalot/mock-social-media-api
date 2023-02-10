from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
