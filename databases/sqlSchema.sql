-- Drop Tables if they exist
DROP TABLE IF EXISTS tumor_mean;
DROP TABLE IF EXISTS tumor_se;
DROP TABLE IF EXISTS tumor_worst;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS patient_changes_log;

-- Create Patients Table
CREATE TABLE IF NOT EXISTS patients (
    serial_id SERIAL PRIMARY KEY, -- Auto-incremented ID to track insertion order
    id VARCHAR(50) UNIQUE NOT NULL, -- String-based ID to connect all tables
    diagnosis VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tumor Mean Table
CREATE TABLE IF NOT EXISTS tumor_mean (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(id) ON DELETE CASCADE,
    radius_mean FLOAT, texture_mean FLOAT, perimeter_mean FLOAT, area_mean FLOAT,
    smoothness_mean FLOAT, compactness_mean FLOAT, concavity_mean FLOAT, concave_points_mean FLOAT,
    symmetry_mean FLOAT, fractal_dimension_mean FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tumor SE Table
CREATE TABLE IF NOT EXISTS tumor_se (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(id) ON DELETE CASCADE,
    radius_se FLOAT, texture_se FLOAT, perimeter_se FLOAT, area_se FLOAT,
    smoothness_se FLOAT, compactness_se FLOAT, concavity_se FLOAT, concave_points_se FLOAT,
    symmetry_se FLOAT, fractal_dimension_se FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tumor Worst Table
CREATE TABLE IF NOT EXISTS tumor_worst (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(id) ON DELETE CASCADE,
    radius_worst FLOAT, texture_worst FLOAT, perimeter_worst FLOAT, area_worst FLOAT,
    smoothness_worst FLOAT, compactness_worst FLOAT, concavity_worst FLOAT, concave_points_worst FLOAT,
    symmetry_worst FLOAT, fractal_dimension_worst FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Patient Changes Log Table
CREATE TABLE patient_changes_log (
    log_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(id) ON DELETE CASCADE,
    old_diagnosis VARCHAR(10),
    new_diagnosis VARCHAR(10),
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Function to Log Diagnosis Changes
CREATE OR REPLACE FUNCTION log_diagnosis_change() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.diagnosis IS DISTINCT FROM NEW.diagnosis THEN
        INSERT INTO patient_changes_log (patient_id, old_diagnosis, new_diagnosis)
        VALUES (OLD.id, OLD.diagnosis, NEW.diagnosis);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create Trigger to Log Diagnosis Changes
CREATE TRIGGER trigger_log_diagnosis_change
BEFORE UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION log_diagnosis_change();

-- Stored Procedure for Inserting or Updating Patients
DROP PROCEDURE IF EXISTS InsertOrUpdatePatient;

CREATE OR REPLACE PROCEDURE InsertOrUpdatePatient(
    p_id VARCHAR(50),
    p_diagnosis VARCHAR(10),
    OUT p_serial_id INT
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Insert or update the patient record
    INSERT INTO patients (id, diagnosis)
    VALUES (p_id, p_diagnosis)
    ON CONFLICT (id) DO UPDATE SET diagnosis = EXCLUDED.diagnosis
    RETURNING serial_id INTO p_serial_id;
END;
$$;
