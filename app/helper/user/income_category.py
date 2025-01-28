from app.model.user.income_category import ModelUserIncomeCategory
from app.model.user.user import ModelUser
from app.database import engine
from sqlalchemy.orm import Session
from app.helper.response import HelperResponse
from sqlalchemy import func

class HelperUserIncomeCategory:
    @staticmethod
    def init_expense_category():
        ModelUserIncomeCategory.metadata.create_all(bind=engine)
    
    @staticmethod
    def is_like_category_exists(db: Session, user: ModelUser, title: str) -> bool:
        existing_category = db.query(ModelUserIncomeCategory).filter(
            ModelUserIncomeCategory.userid == user.id,
            func.lower(ModelUserIncomeCategory.title) == func.lower(title)
        ).first()
        return existing_category is not None

    
    @staticmethod
    def create_expense_category(db: Session, user: ModelUser, title: str) -> HelperResponse:
        new_expense_category = ModelUserIncomeCategory(userid=user.id, title=title)
        try:
            db.add(new_expense_category)
            db.commit()
            return HelperResponse.success(data=new_expense_category)
        except Exception as e:
            db.rollback()  
            return HelperResponse.error(err_message=str(e))
        finally:
            db.close() 