from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import random
import string
from database import get_connection
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Pydantic models for request/response validation
class TumorMean(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float

class TumorSE(BaseModel):
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float

class TumorWorst(BaseModel):
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

class Patient(BaseModel):
    id: Optional[str] = None
    diagnosis: str
    tumor_mean: TumorMean
    tumor_se: TumorSE
    tumor_worst: TumorWorst

# Function that generate a unique 5-6 digit ID
def generate_unique_id():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    while True:
        # Generate a random 5-6 digit ID
        patient_id = ''.join(random.choices(string.digits, k=random.randint(5, 6)))
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
            if not cursor.fetchone():
                return patient_id

# Root Endpoint - Get all patients
@app.get("/")
def get_all_data():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            # Fetch all patients
            cursor.execute("SELECT * FROM patients")
            patients = cursor.fetchall()

            all_data = []
            for patient in patients:
                patient_id = patient["id"]

                # Fetch tumor data
                cursor.execute("SELECT * FROM tumor_mean WHERE id = %s", (patient_id,))
                tumor_mean = cursor.fetchone()

                cursor.execute("SELECT * FROM tumor_se WHERE id = %s", (patient_id,))
                tumor_se = cursor.fetchone()

                cursor.execute("SELECT * FROM tumor_worst WHERE id = %s", (patient_id,))
                tumor_worst = cursor.fetchone()

                patient_data = {
                    "patient": patient,
                    "tumor_mean": tumor_mean,
                    "tumor_se": tumor_se,
                    "tumor_worst": tumor_worst,
                }
                all_data.append(patient_data)

            return all_data

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            conn.close()

# Get the last inserted patient record
@app.get("/patients/last")
def get_last_patient():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get the last inserted patient
            cursor.execute("SELECT * FROM patients ORDER BY serial_id DESC LIMIT 1")
            patient = cursor.fetchone()

            if not patient:
                raise HTTPException(status_code=404, detail="No patients found")

            patient_id = patient["id"]

            # Fetch tumor data
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
                "tumor_worst": tumor_worst,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

# Get a patient by ID
@app.get("/patients/{patient_id}")
def read_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            # Fetch patient
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cursor.fetchone()

            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")

            # Fetch tumor data
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
                "tumor_worst": tumor_worst,
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            conn.close()

# Create a new patient
@app.post("/patients/")
def create_patient(patient: Patient):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    with conn.cursor() as cursor:
        try:
            # Generate a unique ID if not provided
            if not patient.id:
                patient.id = generate_unique_id()

            # Insert patient
            cursor.execute(
                "INSERT INTO patients (id, diagnosis) VALUES (%s, %s)",
                (patient.id, patient.diagnosis)
            )

            # Insert tumor data
            cursor.execute(
                """
                INSERT INTO tumor_mean (
                    id, radius_mean, texture_mean, perimeter_mean, area_mean, 
                    smoothness_mean, compactness_mean, concavity_mean, concave_points_mean, 
                    symmetry_mean, fractal_dimension_mean
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (patient.id, *patient.tumor_mean.dict().values())
            )

            cursor.execute(
                """
                INSERT INTO tumor_se (
                    id, radius_se, texture_se, perimeter_se, area_se, 
                    smoothness_se, compactness_se, concavity_se, concave_points_se, 
                    symmetry_se, fractal_dimension_se
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (patient.id, *patient.tumor_se.dict().values())
            )

            cursor.execute(
                """
                INSERT INTO tumor_worst (
                    id, radius_worst, texture_worst, perimeter_worst, area_worst, 
                    smoothness_worst, compactness_worst, concavity_worst, concave_points_worst, 
                    symmetry_worst, fractal_dimension_worst
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (patient.id, *patient.tumor_worst.dict().values())
            )

            conn.commit()
            return {"message": "Patient created successfully", "id": patient.id}

        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            conn.close()

# Update a patient's details
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    with conn.cursor() as cursor:
        try:
            # Update patient
            cursor.execute(
                "UPDATE patients SET diagnosis = %s WHERE id = %s",
                (patient.diagnosis, patient_id)
            )

            # Update tumor data
            cursor.execute(
                """
                UPDATE tumor_mean SET 
                    radius_mean = %s, texture_mean = %s, perimeter_mean = %s, area_mean = %s, 
                    smoothness_mean = %s, compactness_mean = %s, concavity_mean = %s, 
                    concave_points_mean = %s, symmetry_mean = %s, fractal_dimension_mean = %s 
                WHERE id = %s
                """,
                (*patient.tumor_mean.dict().values(), patient_id)
            )

            cursor.execute(
                """
                UPDATE tumor_se SET 
                    radius_se = %s, texture_se = %s, perimeter_se = %s, area_se = %s, 
                    smoothness_se = %s, compactness_se = %s, concavity_se = %s, 
                    concave_points_se = %s, symmetry_se = %s, fractal_dimension_se = %s 
                WHERE id = %s
                """,
                (*patient.tumor_se.dict().values(), patient_id)
            )

            cursor.execute(
                """
                UPDATE tumor_worst SET 
                    radius_worst = %s, texture_worst = %s, perimeter_worst = %s, area_worst = %s, 
                    smoothness_worst = %s, compactness_worst = %s, concavity_worst = %s, 
                    concave_points_worst = %s, symmetry_worst = %s, fractal_dimension_worst = %s 
                WHERE id = %s
                """,
                (*patient.tumor_worst.dict().values(), patient_id)
            )

            conn.commit()
            return {"message": "Patient updated successfully"}

        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            conn.close()

# Delete a patient by ID
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    with conn.cursor() as cursor:
        try:
            # Delete tumor data
            cursor.execute("DELETE FROM tumor_mean WHERE id = %s", (patient_id,))
            cursor.execute("DELETE FROM tumor_se WHERE id = %s", (patient_id,))
            cursor.execute("DELETE FROM tumor_worst WHERE id = %s", (patient_id,))

            # Delete patient
            cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))

            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Patient not found")

            return {"message": "Patient deleted successfully"}

        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            conn.close()
