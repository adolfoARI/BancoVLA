from fastapi import APIRouter, Depends
import MODELS.etlUsuarios as etlUsuario
import BLL.lnUsuarios as lnUsuario
import MODELS.etlsecurity as etlSecurity
import MODELS.etlapiResponse as etlApiResponse

router = APIRouter(
    prefix="/usuarios", 
    tags=["Usuarios"]
)

@router.post("/login")
def login(credentials: etlUsuario.LoginModel):
    response = lnUsuario.login(credentials.username, credentials.password)
    return response

@router.post("/CreateNewUser")
def createNewUser(user:etlUsuario.UserCreateModel, currentUser: str = Depends(etlSecurity.get_current_user)):
    response = lnUsuario.createUser(user)
    return response

@router.post("/GetAllUsers")
def getAllUsers(currentUser: str = Depends(etlSecurity.get_current_user)):
    response = lnUsuario.getAllUsers()
    return response

@router.post("/refresh")
def refresh_token(currentUser: str = Depends(etlSecurity.get_current_user_from_refresh_token)):
    newAccessToken = etlSecurity.create_access_token(data={"sub": currentUser})

    return etlApiResponse.ApiResponse(
        data = etlUsuario.TokenModel(
            access_token=newAccessToken, 
            refresh_token="", 
            token_type="bearer"
        )
    )