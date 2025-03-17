from pydantic import BaseModel

class PatientBase(BaseModel):
    id: str
    diagnosis: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    diagnosis: str

class PatientResponse(PatientBase):
    class Config:
        from_attributes = True
