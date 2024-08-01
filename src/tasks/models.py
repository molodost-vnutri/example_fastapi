from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String, index=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    public = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='tasks')