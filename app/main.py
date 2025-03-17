from fastapi import FastAPI, HTTPException, Depends
from .database import get_connection
from .schemas import Patient

app = FastAPI()

# Root Endpoint - Get all patients
@app.get("/")
def root():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        # Fetch all records from the Patients table
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()
        return {"patients": patients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# CREATE - Insert a new patient
@app.post("/patients/")
def create_patient(patient: Patient):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Patients (id, diagnosis) VALUES (%s, %s)", (patient.id, patient.diagnosis))
        conn.commit()
        return {"message": "Patient added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# READ - Get a patient by ID
@app.get("/patients/{patient_id}")
def read_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        if patient:
            return patient
        raise HTTPException(status_code=404, detail="Patient not found")
    finally:
        cursor.close()
        conn.close()

# UPDATE - Update a patient's diagnosis
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Patients SET diagnosis = %s WHERE id = %s", (patient.diagnosis, patient_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient updated successfully"}
    finally:
        cursor.close()
        conn.close()

# DELETE - Remove a patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Patients WHERE id = %s", (patient_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully"}
    finally:
        cursor.close()
        conn.close()

# Run the FastAPI app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
