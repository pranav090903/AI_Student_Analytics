from pydantic import BaseModel

class RegisterUser(BaseModel):
    username: str
    password: str
    role: str


class LoginUser(BaseModel):
    username: str
    password: str
