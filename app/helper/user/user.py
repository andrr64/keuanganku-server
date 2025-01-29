from app.model.user.user import ModelUser
from app.model.user.information import ModelUserInformation
from sqlalchemy.orm import Session
from app.helper.response import HelperResponse

name_list = ["John", "Jane", "Alice", "Bob", "Charlie"]

class HelperUser:
    @staticmethod
    def create_user(db: Session, new_user: ModelUser, name: str= None) -> HelperResponse:
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            user_info = ModelUserInformation(name=name, userid=new_user.id)
            db.add(user_info)
            db.commit()
            
            return HelperResponse.success(message='User created successfully', data=new_user)
        except Exception as e:
            db.rollback()
            return HelperResponse.error(err_message=f"An error occurred: {str(e)}")

    @staticmethod
    def read_user_by_id(db: Session, id: str):
        try:
            data: ModelUser= db.query(ModelUser).filter(ModelUser.id == id).first()
            return HelperResponse.success(data=data)
        except Exception as e:
            return HelperResponse.error(err_message=f"An error occured: {str(e)}")

    @staticmethod
    def read_user_by_username(db:Session, username: str) -> HelperResponse:
        try:
            data: ModelUser = db.query(ModelUser).filter(ModelUser.username == username).first()
            return HelperResponse.success(data=data)
        except Exception as e:
            return HelperResponse.error(err_message=f"An error occured: {str(e)}")