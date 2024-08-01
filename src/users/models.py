from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    tasks = relationship('Tasks', back_populates='user')