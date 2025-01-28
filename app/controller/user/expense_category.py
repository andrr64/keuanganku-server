from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.expense_category import HelperUserExpenseCategory
from fastapi import status
from app.helper.user.user import HelperUser
from app.model.user.expense_category import ModelUserExpenseCategory

class ControllerUserExpenseCategory:
    @staticmethod
    def add_expense_category(db: Session, user_id: str, title: str) -> ControllerResponse:
        # Mencari user
        user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
        if not user:
            return ControllerResponse.not_found(err_message="Unknown Account or Invalid Token")
        
        # Periksa apakah kategory dengan nama yang mirip sudah ada?
        category_already_exists = HelperUserExpenseCategory.is_like_category_exists(db=db, user=user, title=title)
        if category_already_exists:
            return ControllerResponse.conflict(err_message="Category already exists")
        
        insert_exp_category = HelperUserExpenseCategory.create_expense_category(db=db, user=user, title=title)
        
        if not insert_exp_category.success:
            return ControllerResponse.error(err_message=insert_exp_category.message)
    
        return ControllerResponse.success(
            data=insert_exp_category.data
        )
        
    @staticmethod
    def get_expense_category(db: Session, user_id: str) -> ControllerResponse:
        user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
        if not user:
            return ControllerResponse.not_found("Unknown User")
        
        # Misalnya expense_categories adalah list dari dictionary
        filtered_categories = []
        for category in user.expense_categories:
            category_dict = category.__dict__  
            category_dict.pop("createdAt", None)  
            category_dict.pop("userid", None)    
            filtered_categories.append(category_dict)

        return ControllerResponse.success(
            data=filtered_categories
        )