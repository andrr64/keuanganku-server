from sqlalchemy import ForeignKey, DateTime, Column, String
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ModelUserIncomeCategory(Base):
    __tablename__ = "user_income_category"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    userid = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String(50), nullable=False)
    
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("ModelUser", back_populates="income_categories")

def filter_data(income: ModelUserIncomeCategory) -> dict:
    return {
        "id": income.id,
        "title": income.title,
    }