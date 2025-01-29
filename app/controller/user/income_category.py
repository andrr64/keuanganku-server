from sqlalchemy.orm import Session
from app.model.user.user import ModelUser
from app.controller.user.user import  ControllerResponse
from app.helper.user.income_category import HelperUserIncomeCategory
from app.model.user.income_category import filter_data
from fastapi import status, HTTPException

class ControllerUserIncomeCategory:
    @staticmethod
    def add_income_category(db: Session, user_id: str, title: str) -> ControllerResponse:
        user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
        if not user:
            return ControllerResponse.not_found(err_message="Unknown Account or Invalid Token")
        category_already_exists = HelperUserIncomeCategory.is_like_category_exists(db=db, user=user, title=title)
        if category_already_exists:
            return ControllerResponse.conflict(err_message="Category already exists")
        
        insert_inc_category = HelperUserIncomeCategory.create_income_category(db=db, user=user, title=title)
        if not insert_inc_category.success:
            return ControllerResponse.error(err_message=insert_inc_category.message)
        
        return ControllerResponse.success(
            data=filter_data(insert_inc_category.data)
        )
        
    @staticmethod
    def get_income_category(db: Session, user_id: str) -> ControllerResponse:
        user = db.query(ModelUser).filter(ModelUser.id == user_id).first()
        if not user:
            return ControllerResponse.not_found("Unknown User")
        
        # Misalnya expense_categories adalah list dari dictionary
        return ControllerResponse.success(
            data=[filter_data(x) for x in user.income_categories]
        )