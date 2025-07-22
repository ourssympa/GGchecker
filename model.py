from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
