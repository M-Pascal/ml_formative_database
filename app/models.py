from sqlalchemy import Column, String
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    diagnosis = Column(String)
