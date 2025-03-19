import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Load the dataset
csv_file = "../dataset/data.csv"
df = pd.read_csv(csv_file, skipinitialspace=True)  # Fix column name spacing issues

# Rename columns to replace spaces with underscores
df.columns = df.columns.str.replace(" ", "_")

# Validate columns
required_columns = {
    "id", "diagnosis", "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
    "smoothness_mean", "compactness_mean", "concavity_mean", "concave_points_mean",
    "symmetry_mean", "fractal_dimension_mean", "radius_se", "texture_se",
    "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se",
    "concave_points_se", "symmetry_se", "fractal_dimension_se", "radius_worst",
    "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave_points_worst",
    "symmetry_worst", "fractal_dimension_worst"
}

if not required_columns.issubset(df.columns):
    missing_cols = required_columns - set(df.columns)
    print(f"Error: Missing columns in dataset: {missing_cols}")
    exit(1)

# Get DATABASE_URL from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env file")
    exit(1)

# Parse database URL
try:
    result = urlparse(DATABASE_URL)
    db_params = {
        "dbname": result.path[1:],  # Remove leading slash
        "user": result.username,
        "password": result.password,
        "host": result.hostname,
        "port": result.port or 5432
    }
except Exception as e:
    print(f"Error parsing DATABASE_URL: {e}")
    exit(1)

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    print("Connected to PostgreSQL")

    # Check if tables exist
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_name IN ('patients', 'tumor_mean', 'tumor_se', 'tumor_worst');
    """)
    existing_tables = {row[0] for row in cursor.fetchall()}

    required_tables = {'patients', 'tumor_mean', 'tumor_se', 'tumor_worst'}
    if not required_tables.issubset(existing_tables):
        print("Error: Some required tables are missing in the database.")
        exit(1)

    # SQL queries
    insert_patient = """
    INSERT INTO patients (id, diagnosis)
    VALUES (%s, %s)
    ON CONFLICT (id) DO UPDATE SET diagnosis = EXCLUDED.diagnosis;
    """

    insert_tumor_mean = """
    INSERT INTO tumor_mean (
        id, radius_mean, texture_mean, perimeter_mean, area_mean, 
        smoothness_mean, compactness_mean, concavity_mean, concave_points_mean, 
        symmetry_mean, fractal_dimension_mean
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    insert_tumor_se = """
    INSERT INTO tumor_se (
        id, radius_se, texture_se, perimeter_se, area_se, 
        smoothness_se, compactness_se, concavity_se, concave_points_se, 
        symmetry_se, fractal_dimension_se
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    insert_tumor_worst = """
    INSERT INTO tumor_worst (
        id, radius_worst, texture_worst, perimeter_worst, area_worst, 
        smoothness_worst, compactness_worst, concavity_worst, concave_points_worst, 
        symmetry_worst, fractal_dimension_worst
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    # Insert data into PostgreSQL
    for index, row in df.iterrows():
        patient_id = str(row["id"])  # Convert to string for consistency
        print(f"Inserting row {index + 1} (ID: {patient_id})...")

        try:
            # Start a transaction
            cursor.execute("BEGIN;")

            # Insert or update patient
            cursor.execute(insert_patient, (patient_id, row["diagnosis"]))

            # Insert tumor data
            cursor.execute(insert_tumor_mean, (
                patient_id, row["radius_mean"], row["texture_mean"], row["perimeter_mean"], row["area_mean"],
                row["smoothness_mean"], row["compactness_mean"], row["concavity_mean"], row["concave_points_mean"],
                row["symmetry_mean"], row["fractal_dimension_mean"]
            ))

            cursor.execute(insert_tumor_se, (
                patient_id, row["radius_se"], row["texture_se"], row["perimeter_se"], row["area_se"],
                row["smoothness_se"], row["compactness_se"], row["concavity_se"], row["concave_points_se"],
                row["symmetry_se"], row["fractal_dimension_se"]
            ))

            cursor.execute(insert_tumor_worst, (
                patient_id, row["radius_worst"], row["texture_worst"], row["perimeter_worst"], row["area_worst"],
                row["smoothness_worst"], row["compactness_worst"], row["concavity_worst"], row["concave_points_worst"],
                row["symmetry_worst"], row["fractal_dimension_worst"]
            ))

            # Commit the transaction
            conn.commit()
        except KeyError as ke:
            conn.rollback()  # Rollback on error
            print(f"KeyError: Missing column {ke} in row {index + 1} (ID: {patient_id}). Check dataset structure.")
        except psycopg2.Error as e:
            conn.rollback()  # Rollback on error
            print(f"Database error inserting row {index + 1} (ID: {patient_id}): {e}")

    print("Data successfully inserted into Database.")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("PostgreSQL connection closed.")
