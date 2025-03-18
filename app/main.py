from fastapi import FastAPI, HTTPException, Depends
from app.database import get_connection
from app.schemas import Patient


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
        # Insert into Patients table
        cursor.execute("INSERT INTO Patients (id, diagnosis) VALUES (%s, %s)", (patient.id, patient.diagnosis))
        
        # Insert into Tumor Mean table
        cursor.execute("INSERT INTO tumor_mean (id, radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean, compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (patient.id, patient.tumor_mean.radius_mean, patient.tumor_mean.texture_mean, patient.tumor_mean.perimeter_mean, patient.tumor_mean.area_mean, patient.tumor_mean.smoothness_mean, 
                        patient.tumor_mean.compactness_mean, patient.tumor_mean.concavity_mean, patient.tumor_mean.concave_points_mean, patient.tumor_mean.symmetry_mean, patient.tumor_mean.fractal_dimension_mean))

        # Insert into Tumor SE table
        cursor.execute("INSERT INTO tumor_se (id, radius_se, texture_se, perimeter_se, area_se, smoothness_se, compactness_se, concavity_se, concave_points_se, symmetry_se, fractal_dimension_se) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (patient.id, patient.tumor_se.radius_se, patient.tumor_se.texture_se, patient.tumor_se.perimeter_se, patient.tumor_se.area_se, patient.tumor_se.smoothness_se, 
                        patient.tumor_se.compactness_se, patient.tumor_se.concavity_se, patient.tumor_se.concave_points_se, patient.tumor_se.symmetry_se, patient.tumor_se.fractal_dimension_se))

        # Insert into Tumor Worst table
        cursor.execute("INSERT INTO tumor_worst (id, radius_worst, texture_worst, perimeter_worst, area_worst, smoothness_worst, compactness_worst, concavity_worst, concave_points_worst, symmetry_worst, fractal_dimension_worst) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (patient.id, patient.tumor_worst.radius_worst, patient.tumor_worst.texture_worst, patient.tumor_worst.perimeter_worst, patient.tumor_worst.area_worst, patient.tumor_worst.smoothness_worst,
                        patient.tumor_worst.compactness_worst, patient.tumor_worst.concavity_worst, patient.tumor_worst.concave_points_worst, patient.tumor_worst.symmetry_worst, patient.tumor_worst.fractal_dimension_worst))

        conn.commit()
        return {"message": "Patient added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# READ - Get a patient by ID with related tumor data
@app.get("/patients/{patient_id}")
def read_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Fetch related tumor data
        cursor.execute("SELECT * FROM tumor_mean WHERE id = %s", (patient_id,))
        tumor_mean = cursor.fetchone()

        cursor.execute("SELECT * FROM tumor_se WHERE id = %s", (patient_id,))
        tumor_se = cursor.fetchone()

        cursor.execute("SELECT * FROM tumor_worst WHERE id = %s", (patient_id,))
        tumor_worst = cursor.fetchone()

        return {
            "patient": patient,
            "tumor_mean": tumor_mean,
            "tumor_se": tumor_se,
            "tumor_worst": tumor_worst
        }
    finally:
        cursor.close()
        conn.close()

# ====================
@app.get("/patients/latest")
def get_latest_patient():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
   
    cursor = conn.cursor()
    try:
        # Get the latest patient ID
        cursor.execute("SELECT MAX(id) FROM Patients")
        latest_id = cursor.fetchone()[0]

        print(f"DEBUG: Latest Patient ID: {latest_id}")  # Debugging

        if not latest_id:
            raise HTTPException(status_code=404, detail="No patient data found")

        # Fetch the patient record using latest_id
        cursor.execute("SELECT * FROM Patients WHERE id = %s", (latest_id,))
        patient = cursor.fetchone()

        print(f"DEBUG: Patient Data: {patient}")  # Debugging

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Fetch related tumor data
        cursor.execute("SELECT * FROM tumor_mean WHERE id = %s", (latest_id,))
        tumor_mean = cursor.fetchone()
        print(f"DEBUG: Tumor Mean: {tumor_mean}")  # Debugging

        cursor.execute("SELECT * FROM tumor_se WHERE id = %s", (latest_id,))
        tumor_se = cursor.fetchone()
        print(f"DEBUG: Tumor SE: {tumor_se}")  # Debugging

        cursor.execute("SELECT * FROM tumor_worst WHERE id = %s", (latest_id,))
        tumor_worst = cursor.fetchone()
        print(f"DEBUG: Tumor Worst: {tumor_worst}")  # Debugging

        return {
            "id": patient[0],
            "diagnosis": patient[1],
            "tumor_mean": tumor_mean,
            "tumor_se": tumor_se,
            "tumor_worst": tumor_worst,
        }
    finally:
        cursor.close()
        conn.close()



# ==========

# UPDATE - Update a patient's diagnosis and tumor data
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        # Update Patients table
        cursor.execute("UPDATE Patients SET diagnosis = %s WHERE id = %s", (patient.diagnosis, patient_id))

        # Update Tumor Mean table
        cursor.execute("UPDATE tumor_mean SET radius_mean = %s, texture_mean = %s, perimeter_mean = %s, area_mean = %s, smoothness_mean = %s, compactness_mean = %s, concavity_mean = %s, concave_points_mean = %s, symmetry_mean = %s, fractal_dimension_mean = %s WHERE id = %s", 
                       (patient.tumor_mean.radius_mean, patient.tumor_mean.texture_mean, patient.tumor_mean.perimeter_mean, patient.tumor_mean.area_mean, patient.tumor_mean.smoothness_mean, 
                        patient.tumor_mean.compactness_mean, patient.tumor_mean.concavity_mean, patient.tumor_mean.concave_points_mean, patient.tumor_mean.symmetry_mean, patient.tumor_mean.fractal_dimension_mean, patient_id))

        # Update Tumor SE table
        cursor.execute("UPDATE tumor_se SET radius_se = %s, texture_se = %s, perimeter_se = %s, area_se = %s, smoothness_se = %s, compactness_se = %s, concavity_se = %s, concave_points_se = %s, symmetry_se = %s, fractal_dimension_se = %s WHERE id = %s",
                       (patient.tumor_se.radius_se, patient.tumor_se.texture_se, patient.tumor_se.perimeter_se, patient.tumor_se.area_se, patient.tumor_se.smoothness_se, 
                        patient.tumor_se.compactness_se, patient.tumor_se.concavity_se, patient.tumor_se.concave_points_se, patient.tumor_se.symmetry_se, patient.tumor_se.fractal_dimension_se, patient_id))

        # Update Tumor Worst table
        cursor.execute("UPDATE tumor_worst SET radius_worst = %s, texture_worst = %s, perimeter_worst = %s, area_worst = %s, smoothness_worst = %s, compactness_worst = %s, concavity_worst = %s, concave_points_worst = %s, symmetry_worst = %s, fractal_dimension_worst = %s WHERE id = %s",
                       (patient.tumor_worst.radius_worst, patient.tumor_worst.texture_worst, patient.tumor_worst.perimeter_worst, patient.tumor_worst.area_worst, patient.tumor_worst.smoothness_worst,
                        patient.tumor_worst.compactness_worst, patient.tumor_worst.concavity_worst, patient.tumor_worst.concave_points_worst, patient.tumor_worst.symmetry_worst, patient.tumor_worst.fractal_dimension_worst, patient_id))

        conn.commit()
        return {"message": "Patient updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# DELETE - Remove a patient and their related tumor data
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = conn.cursor()
    try:
        # Delete related tumor data first
        cursor.execute("DELETE FROM tumor_mean WHERE id = %s", (patient_id,))
        cursor.execute("DELETE FROM tumor_se WHERE id = %s", (patient_id,))
        cursor.execute("DELETE FROM tumor_worst WHERE id = %s", (patient_id,))

        # Then delete the patient record
        cursor.execute("DELETE FROM Patients WHERE id = %s", (patient_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return {"message": "Patient and related data deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
