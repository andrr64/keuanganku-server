import jwt
import os
from helper.response import HelperResponse
from model.user import ModelUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from dotenv import load_dotenv
from helper.user import HelperUser
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from controller.response import ControllerResponse

load_dotenv()

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

class ControllerUser:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    access_token_expired = timedelta(minutes=3)
    
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
            return HelperResponse.error_response("Invalid username or password")
        
        if not ControllerUser.__pwd_context.verify(password, existing_user.password):
            return HelperResponse.error_response("Invalid username or password")
        
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
    def create_access_token(data: dict, expires_delta: timedelta = access_token_expired) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")