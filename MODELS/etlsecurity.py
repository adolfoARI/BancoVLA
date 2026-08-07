import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import bcrypt
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import MODELS.etlexceptions as etlException

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES",30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS",7))

#Contexto para poder hashear/verificar las contrasenas con bycrypt
bearer_schema =HTTPBearer()

# Dos metodos que tienen que ver con contrasenas
def hash_password(password: str) -> str:
    #Convierte la contrasena en hash al crear un usuario
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Compara la contrasena en texto plano contra el hash guardado
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data:dict, expires_delta:timedelta | None = None)->str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> str:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise etlException.BusinessError(1006, "Token inválido")

        return username
    except JWTError:
        raise etlException.BusinessError(1007, "Token inválido o expirado", 401)

def create_refresh_token(data:dict, expires_delta:timedelta | None = None)->str:
    to_encode = data.copy()  

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_from_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> str:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise etlException.BusinessError(1006, "Token inválido")

        return username
    except JWTError:
        raise etlException.BusinessError(1007, "Token inválido o expirado")

