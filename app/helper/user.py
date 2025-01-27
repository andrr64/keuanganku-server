from model.user import ModelUser
from model.user_info import ModelUserInformation
from sqlalchemy.orm import Session
from helper.response import HelperResponse
from dotenv import load_dotenv

load_dotenv()

class HelperUser:
    @staticmethod
    def create_user(db: Session, new_user: ModelUser) -> HelperResponse:
        try:
            # Menambahkan user ke dalam DB
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            user_info = ModelUserInformation(userid=new_user.id)
            db.add(user_info)
            db.commit()
            
            return HelperResponse.success(message='User created successfully', data=new_user)
        except Exception as e:
            db.rollback()
            return HelperResponse.error(err_message=f"An error occurred: {str(e)}")
        
    @staticmethod
    def read_user_by_username(db:Session, username: str) -> HelperResponse:
        try:
            data: ModelUser = db.query(ModelUser).filter(ModelUser.username == username).first()
            return HelperResponse.success(data=data)
        except Exception as e:
            return HelperResponse.error(err_message=f"An error occured: {str(e)}")