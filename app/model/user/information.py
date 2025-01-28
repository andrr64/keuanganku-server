from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import datetime
from sqlalchemy.orm import relationship
import uuid

class ModelUserInformation(Base):
    __tablename__ = "user_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    userid = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True)
    name = Column(String(100), nullable=False, default="")
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("ModelUser", back_populates="information")