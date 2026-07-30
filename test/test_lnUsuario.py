from unittest.mock import patch
import BLL.lnUsuarios as lnUsuario
import MODELS.etlUsuarios as etlUsuario

#SumarDosNumerosPositvos
def test_sumTwoPositivesNumbers():
    num1: int = 3
    num2: int = 2
    esperado = 5
    real = lnUsuario.sumTwoNumbers(num1, num2)
    assert esperado == real

def test_sumTwoNegativesNumbers1():
    num1: int = -3
    num2: int = -2
    esperado = -5
    real = lnUsuario.sumTwoNumbers(num1, num2)
    assert esperado == real

def test_ValidateAterNewUsert_1():
    user1 =  etlUsuario.UserCreateModel(name= "Adolfo", age= 33, active= True, username = "ado21")
    user2 =  etlUsuario.UserCreateModel(name= "Adolfo", age= 33, active= True, username = "ado21")

    real = lnUsuario.alterCreateUser(user1)
    assert real == user2

def make_user(**overrides):
    data = { "name" : "Adolfo", "age":33, "active": True, "username": "ado21"}
    data.update(overrides)
    return etlUsuario.UserCreateModel(**data)

@patch("BLL.lnUsuarios.adUsuario")
def test_createUser_username_yaexiste(mock_adUsuario):
    mock_adUsuario.existUser.return_value = True
    
    real = lnUsuario.createUser(make_user())
    esperado = "El username ya existe"

    assert real == esperado
    mock_adUsuario.createUser.assert_not_called()

@patch("BLL.lnUsuarios.adUsuario")
def test_createUser_age_menorEdad(mock_adUsuario):
    mock_adUsuario.existUser.return_value = False
    
    real = lnUsuario.createUser(make_user(age= 17))
    esperado = "La edad debe ser mayor de 18 años"

    assert real == esperado
    mock_adUsuario.createUser.assert_not_called()

@patch("BLL.lnUsuarios.adUsuario")
def test_createUser(mock_adUsuario):
    mock_adUsuario.existUser.return_value = False
    
    user = make_user()
    real = lnUsuario.createUser(user)
    esperado = "Usuario creado"

    assert real == esperado
    mock_adUsuario.createUser.assert_called_once_with(user)