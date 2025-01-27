from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user import ControllerUser
from app.controller.response import ControllerResponse
from starlette import status as HTTPStatus
import os


debug = os.getenv('debug') == 'yes'
router = APIRouter()

class FormRegisterUser(BaseModel):
    username: str
    password: str
    
class FormLoginUser(BaseModel):
    username: str
    password: str
    
class FormUpdateUser(BaseModel):
    username: str
    new_username: str | None = None
    new_password: str | None = None
    name: str
    
def sendResponse(controllerResponse: ControllerResponse) -> any:
    if (controllerResponse.success):
        return controllerResponse.to_dict()
    raise HTTPException(
        status_code=controllerResponse.http_code,
        detail=controllerResponse.message
    )

# Endpoint untuk register
@router.post("/register")
async def register_user(user: FormRegisterUser, db: Session = Depends(get_db)):
    response: ControllerResponse = ControllerUser.create_user(
        db=db, 
        username=user.username, 
        password=user.password
    )
    
    if response.success:
        return {"message": response.message}
    else:
        raise HTTPException(
            status_code=response.http_code,  # Gunakan status code dari HelperResponse
            detail=response.message  # Gunakan pesan dari HelperResponse
        )
        
# Endpoint untuk login
@router.post("/login")
async def login_user(user: FormLoginUser, db: Session = Depends(get_db), response: Response= None):
    response_data = ControllerUser.login_user(db=db, username=user.username, password=user.password)
    if (response_data.success):
        token = response_data.data["access_token"]
        response.set_cookie(
            key="access_token", # Nama cookie
            value=token,        # Nilai token JWT
            httponly=True,      # Menghindari akses dari JavaScript
            secure=debug,        # Hanya untuk koneksi HTTPS
            samesite="Strict",  # Menghindari CSRF
            max_age=ControllerUser.access_token_expired,  # Set waktu kadaluarsa cookie (misal 1 jam)
        )
    return sendResponse(response_data)

@router.put('/update')
async def update_userinfo(request: Request, form: FormUpdateUser, db: Session= Depends(get_db), response: Response = None):
    access_token = request.cookies.get("access_token")
    controllerResponse = ControllerUser.update_userinfo(
        db=db,
        token=access_token,
        oldUsername=form.username,
        new_username=form.new_username,
        new_password=form.new_password,
        name=form.name 
    )
    if controllerResponse.http_code == HTTPStatus.HTTP_401_UNAUTHORIZED:
        response.delete_cookie(
            key="access_token",  # Nama cookie yang ingin dihapus
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        raise HTTPException(
            status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    elif not controllerResponse.success:
        raise HTTPException(
            status_code=controllerResponse.http_code,
            detail=controllerResponse.message
        )
    return sendResponse(controllerResponse)

# Endpoint untuk cek token
@router.post('/check-token')
async def check_token(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")  # Mengambil access_token dari cookie
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Access token is missing"
        )

    checktoken_response = ControllerUser.is_accesstoken_valid(token=access_token)
    if (not checktoken_response.success):
        raise HTTPException(
            status_code=checktoken_response.http_code,
            detail=checktoken_response.message
        )
    username = checktoken_response.data
    return checktoken_response.to_dict()