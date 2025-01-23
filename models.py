from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Register(Login):
    name: str


class Portfolio(BaseModel):
    scheme_code: str