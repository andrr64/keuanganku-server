from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.expense_category import HelperUserExpenseCategory
from app.model.user.expense_category import filter_data

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
            data=filter_data[insert_exp_category.data]
        )
        
    @staticmethod
    def get_expense_category(db: Session, user_id: str) -> ControllerResponse:
        user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
        if not user:
            return ControllerResponse.not_found("Unknown User")
        
        return ControllerResponse.success(
            data=[filter_data(x) for x in user.expense_categories]
        )