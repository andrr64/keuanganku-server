import uuid
from sqlalchemy import ForeignKey, DateTime, Column, String, UUID, CheckConstraint, Numeric
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.orm import relationship

class ModelUserExpense(Base):
    __tablename__ = "user_expense"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userid = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    categoryid = Column(UUID(as_uuid=True), ForeignKey("user_expense_category.id"), nullable=False)
    title = Column(String(50), nullable=False)
    amount = Column(Numeric(precision=15, scale=3), nullable=False)  # Presisi 15, skala 3
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("ModelUser", back_populates="expenses")

    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_amount_min'),
        CheckConstraint('amount <= 1000000000000', name='check_amount_max'),
    )

def filter_data(expense: ModelUserExpense) -> dict:
    return {
        "id": expense.id,
        "title": expense.title,
        "amount": expense.amount,
        "createdAt": expense.createdAt,
        "updatedAt": expense.updatedAt,
    }