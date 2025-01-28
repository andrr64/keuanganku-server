from sqlalchemy import Integer, ForeignKey, DateTime, Column, String
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base

class ModelUserIncomeCategory(Base):
    __tablename__ = "user_income_category"
    
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(50), nullable=False)
    
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    user = relationship("ModelUser", back_populates="income_categories")
