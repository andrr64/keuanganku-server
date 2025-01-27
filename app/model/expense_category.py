from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class ModelExpenseCategory(Base):
    __tablename__ = "expense_category"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))