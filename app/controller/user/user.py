import datetime
import os
import uuid
from app.model.user.user import ModelUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.controller.response import ControllerResponse
from app.helper.user.user import HelperUser
from fastapi import Response
from app.middleware import token as TokenUtil

TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

class ControllerUser:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @staticmethod
    def get_hash_password(pswd: str) -> str:
        return ControllerUser.__pwd_context.hash(pswd)
    
    @staticmethod
    def create_user(db: Session, name: str, username: str, password: str) -> ControllerResponse:
        existing_user = HelperUser.read_user_by_username(db=db, username=username)
        if not (existing_user.data is None):
            return ControllerResponse.bad_request("Username has already exist")
        hashed_password = ControllerUser.__pwd_context.hash(password)
        new_user = ModelUser(username=username, password=hashed_password)

        helper_response = HelperUser.create_user(db=db, new_user=new_user, name=name)
        if helper_response.success:
            return ControllerResponse.success(message="Create user successful")
        return ControllerResponse.error(
            err_message=helper_response.message,
            http_code=500
        )

    @staticmethod
    def update_user(db: Session, user_id: uuid, response: Response, new_username: str | None, new_password: str | None, new_name: str | None) -> ControllerResponse:
        find_user = HelperUser.read_user_by_id(db=db, id=user_id)
        if find_user.data is None:
            return ControllerResponse.not_found()
        user: ModelUser = find_user.data
        user_info = user.information

        if new_username:
            user.username = new_username
        if new_password:
            user.password = ControllerUser.get_hash_password(new_password)
        if new_name:
            user_info.name = new_name
        try:
            user.updatedAt = datetime.datetime.now(datetime.timezone.utc)
            user_info.updatedAt = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            db.refresh(user)
            db.refresh(user_info)
            return ControllerResponse.success(data={
                "username": user.username,
                "name": user_info.name,
                "updatedAt": user.updatedAt,
            })
        except Exception as e:
            db.rollback()
            return ControllerResponse.error(err_message=f"Error while updating user: {str(e)}")


    @staticmethod
    def login_user(db: Session, username: str, password: str, response: Response) -> ControllerResponse:
        find_user = HelperUser.read_user_by_username(db=db, username=username)
        if find_user.data is None:
            return ControllerResponse.not_found(err_message="Invalid username or password")
        user: ModelUser = find_user.data

        if not ControllerUser.__pwd_context.verify(password, user.password):
            return ControllerResponse.error("Invalid username or password")

        # Generate dan set token
        access_token = TokenUtil.create_access_token(user.id)
        TokenUtil.set_access_token(token=access_token, response=response)
        name = user.information.name
        return ControllerResponse.success(message="OK", data={
            "name": name,
            "username": username,
        })