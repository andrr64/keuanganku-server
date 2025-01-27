import jwt
import os
from app.helper.response import HelperResponse
from app.model.user.user import ModelUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.helper.user.user import HelperUser
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from app.controller.response import ControllerResponse
from app.model.user.information import ModelUserInformation
from app.helper.user.user import HelperUser
from starlette import status as HTTPStatus

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

class ControllerUser:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    access_token_expired = timedelta(hours=24)
    
    @staticmethod
    def getHashPassword(pswd: str) -> str:
        return ControllerUser.__pwd_context.hash(pswd)
    
    @staticmethod
    def create_user(db: Session, username: str, password: str) -> ControllerResponse:
        if len(username.strip()) == 0 or len(password.strip()) == 0:
            return ControllerResponse.bad_request(err_message="Username and password can't be empty, Bro.")
        
        existing_user = db.query(ModelUser).filter(ModelUser.username == username).first()
        if existing_user:
            return ControllerResponse.bad_request("Username has already exist")

        if len(password) < 8:
            return ControllerResponse.bad_request("Your password must be at least 8 chars long, Bro.")
        
        hashed_password = ControllerUser.__pwd_context.hash(password)
        new_user = ModelUser(username=username, password=hashed_password)

        createDataResponse = HelperUser.create_user(db=db, new_user=new_user)
        if (createDataResponse.success):
            return ControllerResponse.success(message="Create user successful")
        return ControllerResponse.error(
            err_message=createDataResponse.message,
            http_code=500
        )
    
    @staticmethod
    def login_user(db: Session, username: str, password: str) -> ControllerResponse:
        helperResponse = HelperUser.read_user_by_username(db=db, username=username)
        if (not helperResponse.success):
            return ControllerResponse.error()
            
        existing_user = HelperUser.read_user_by_username(db=db, username=username).data
        if not existing_user:
            return ControllerResponse.error("Invalid username or password")
        
        if not ControllerUser.__pwd_context.verify(password, existing_user.password):
            return ControllerResponse.error("Invalid username or password")
        
        token = ControllerUser.create_access_token(data={"sub": existing_user.username})
        controllerResponse = ControllerResponse.success(
            data={
                "access_token": token,
                "token_type": "bearer"
            },
            message="Login Successful"
        )
        return controllerResponse
        
    @staticmethod
    def create_access_token(data: dict) -> str:
        secret_key = TOKEN_SECRET_KEY
        algorithm = TOKEN_ALGORITHM
        
        expire = datetime.now(timezone.utc) + ControllerUser.access_token_expired
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    @staticmethod
    def update_userinfo(db: Session, token: str, oldUsername: str, new_username: str, new_password: str, name: str):
        decoded_username = ControllerUser.is_accesstoken_valid(token=token)
        if (not decoded_username.success):
            return ControllerResponse.unauthorized(err_message=decoded_username.message)
        
        decoded_username = decoded_username.data
        if (oldUsername != decoded_username):
            return ControllerResponse.unauthorized(err_message='Unauthorized.')
        
        getuserdata: HelperResponse = HelperUser.read_user_by_username(db=db, username=decoded_username)
        if (not getuserdata.data):
            return ControllerResponse.not_found()
       
        user: ModelUser = getuserdata.data
        userinfo: ModelUserInformation= user.user_information
        
        
        if new_username != oldUsername:
            is_user_exists = HelperUser.read_user_by_username(db=db, username=new_username).data
            if (is_user_exists):
                return ControllerResponse.error(
                    err_message="Username already exists", 
                    http_code= HTTPStatus.HTTP_409_CONFLICT
                )
            user.username = new_username
        if new_password:
            user.password = ControllerUser.getHashPassword(new_password)
        if name:
            userinfo.name = name

        db.commit()
        db.refresh(userinfo)

        return ControllerResponse.success(data={
            "username": user.username,
            "name": userinfo.name
        })
        
    @staticmethod
    def is_accesstoken_valid(token: str) -> ControllerResponse:
        """This function will return username or exception"""
        try:
            payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
            username = payload['sub']
            return ControllerResponse.success(data=username)
        except jwt.ExpiredSignatureError:
            return ControllerResponse.unauthorized(err_message="Token has expired")
        except jwt.InvalidTokenError:
            return ControllerResponse.unauthorized(err_message="Invalid token")

    @staticmethod
    def decode_access_token(token: str) -> dict:
        secret_key = TOKEN_SECRET_KEY
        algorithm = TOKEN_ALGORITHM
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )