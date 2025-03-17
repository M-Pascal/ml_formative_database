from sqlalchemy.orm import Session
from models import Patient
from schemas import PatientCreate, PatientUpdate

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(id=patient.id, diagnosis=patient.diagnosis)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: str):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: str, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db_patient.diagnosis = patient.diagnosis
        db.commit()
        db.refresh(db_patient)
        return db_patient
    return None

def delete_patient(db: Session, patient_id: str):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
        return True
    return False
