from app.model.user.user import ModelUser
from app.model.user.information import ModelUserInformation
from sqlalchemy.orm import Session
from app.helper.response import HelperResponse
import random
import uuid

name_list = ["John", "Jane", "Alice", "Bob", "Charlie"]

class HelperUser:
    @staticmethod
    def create_user(db: Session, new_user: ModelUser) -> HelperResponse:
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Generate random number correctly
            random_number = random.randint(1, 10000)
            random_name = f"{random.choice(name_list)}#{random_number}"
            
            # Check if name is within the length limit
            if len(random_name) > 100:
                random_name = random_name[:100]  # Trim to 100 characters if necessary
            
            user_info = ModelUserInformation(name=random_name, userid=new_user.id)
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