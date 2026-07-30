import os
from dotenv import load_dotenv
import psycopg2
import MODELS.etlUsuarios as etlUsuario

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

def getConnection():
    return psycopg2.connect(DATABASE_URL)

def createUser(user: etlUsuario.UserCreateModel, hashedPassword:str):
    conn = getConnection()

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario(nombre, edad, activo, username, password) VALUES(%s, %s, %s, %s, %s);",
                    (user.name, user.age, user.active, user.username, hashedPassword))
        conn.commit()
        cur.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def getAllUsers() -> list[etlUsuario.GetAllUsersModel]:
    conn = getConnection()
    listUser: list[etlUsuario.GetAllUsersModel] = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT idUsuario, nombre, username, activo FROM usuario")
        rowsUser = cur.fetchall()
        cur.close()

        for user in rowsUser:
            newUser = etlUsuario.GetAllUsersModel(
                idUser= user[0], 
                name= user[1], 
                username=user[2], 
                active= user[3]
            )
            listUser.append(newUser)

        return listUser
    finally: 
        conn.close()

def existUser(username:str) -> bool:

    conn = getConnection()

    try:
        cur = conn.cursor()
        cur.execute("SELECT idUsuario FROM usuario WHERE username= %s", (username,))
        result = cur.fetchone()
        cur.close()

        if result is None:
            return False
        else: 
            return True        
    finally: 
        conn.close()

def getUserByUsername(username:str)-> etlUsuario.UserAuthModel:
    conn = getConnection()

    try:
       cur = conn.cursor()
       cur.execute("SELECT idUsuario, username, password, activo FROM usuario WHERE username = %s", (username,))
       result = cur.fetchone()
       cur.close()

       if result is None: 
           return None

       return etlUsuario.UserAuthModel(
            idUser = result[0], 
            username = result[1], 
            password = result[2], 
            active = result[3]
        )
    finally: 
        conn.close()