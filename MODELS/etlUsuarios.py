from pydantic import BaseModel

class UserCreateModel(BaseModel):
    name: str
    age: int
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