from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.database import Base
import uuid


class ModelUserExpenseCategory(Base):
    __tablename__ = "user_expense_category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    userid = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String(50), nullable=False)

    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("ModelUser", back_populates="expense_categories")

def filter_data(income: ModelUserExpenseCategory) -> dict:
    return {
        "id": income.id,
        "title": income.title,
    }