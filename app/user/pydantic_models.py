from pydantic import BaseModel, Field
from typing import Optional

class LoginModel(BaseModel):
    """
    username or password - any one of them will do
    don't have to include both
    """
    username: Optional[str] #= Field(str, regex="^[a-zA-Z0-9_.]{1,200}$")
    email: Optional[str]
    password: str


class SignUpModel(BaseModel):
    name: Optional[str]
    username: str
    email: str
    password: str

class RequestResetPasswordModel(BaseModel):
    email : str

class ResetPasswordModel(BaseModel):
    email: str
    password: str