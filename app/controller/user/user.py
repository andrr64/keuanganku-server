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
from app.controller.user.token import access_token_expired
from fastapi import Response
from app.controller.user.token import set_access_token

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

class ControllerUser:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
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

        helper_response = HelperUser.create_user(db=db, new_user=new_user)
        if helper_response.success:
            return ControllerResponse.success(message="Create user successful")
        return ControllerResponse.error(
            err_message=helper_response.message,
            http_code=500
        )
    
    @staticmethod
    def login_user(db: Session, username: str, password: str, response: Response) -> ControllerResponse:
        helper_response = HelperUser.read_user_by_username(db=db, username=username)
        if not helper_response.success:
            return ControllerResponse.not_found()
            
        existing_user: ModelUser | None = HelperUser.read_user_by_username(db=db, username=username).data
        if not existing_user:
            return ControllerResponse.error("Invalid username or password")
        
        if not ControllerUser.__pwd_context.verify(password, existing_user.password):
            return ControllerResponse.error("Invalid username or password")
        
        token = ControllerUser.create_access_token(data={"sub": existing_user.username})
        set_access_token(token=token, response=response)

        user_info_data: ModelUserInformation= existing_user.information

        controller_response = ControllerResponse.success(
            data={
                "username": existing_user.username,
                "name": user_info_data.name
            }
        )
        return controller_response
        
    @staticmethod
    def create_access_token(data: dict) -> str:
        secret_key = TOKEN_SECRET_KEY
        algorithm = TOKEN_ALGORITHM
        
        expire = datetime.now(timezone.utc) + access_token_expired
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    @staticmethod
    def update_userinfo(db: Session, oldUsername: str, new_username: str, new_password: str, name: str, response: Response):
        getuserdata: HelperResponse = HelperUser.read_user_by_username(db=db, username=oldUsername)
        if (not getuserdata.data):
            return ControllerResponse.not_found()
       
        user: ModelUser = getuserdata.data
        userinfo: ModelUserInformation= user.information
        new_token = None

        if new_username != oldUsername:
            username_taken = HelperUser.read_user_by_username(db=db, username=new_username).data
            if (username_taken):
                return ControllerResponse.conflict(err_message="Username already exists")
            user.username = new_username
            new_token = ControllerUser.create_access_token(data={'sub': new_username})
        if new_password:
            user.password = ControllerUser.getHashPassword(new_password)
        if name:
            userinfo.name = name

        db.commit()
        db.refresh(userinfo)

        if new_token is not None:
            set_access_token(token=new_token, response=response)

        return ControllerResponse.success(data={
            "username": user.username,
            "name": userinfo.name,
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