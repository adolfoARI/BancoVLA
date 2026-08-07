from pydantic import BaseModel
from datetime import date

class UserCreateModel(BaseModel):
    name: str
    birthdate: date
    active: bool
    username : str
    password:str

class GetAllUsersModel(BaseModel):
    idUser: int
    username: str
    name: str
    active: bool

class UserAuthModel(BaseModel):
    idUser: int
    username: str   
    active: bool
    password: str

class TokenModel(BaseModel):
    access_token:str
    refresh_token: str
    token_type: str = "bearer"

class LoginModel(BaseModel):
    username: str
    password:str