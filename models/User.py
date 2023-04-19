from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import datetime

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    gender = Column(String)
    birthday = Column(datetime)
    nationality = Column(String, index=True)
    email = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)

    items = relationship("Item", back_populates="owner")