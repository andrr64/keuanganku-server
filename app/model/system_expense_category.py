from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class ModelSystemExpenseCategory(Base):
    __tablename__ = "system_expense_category"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))