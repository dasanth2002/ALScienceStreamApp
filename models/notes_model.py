from sqlalchemy import Column, Integer, String
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    term = Column(String, index=True)
    content = Column(String, nullable=True)
    file_path = Column(String, nullable=True)  # saved filename
