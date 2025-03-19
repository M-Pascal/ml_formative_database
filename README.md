# Breast Cancer Database Setup and Prediction System

## Overview
This project is designed to create a comprehensive system for managing breast cancer data, including database design, API development, and a machine learning-based prediction system. The system uses both **MySQL** (relational database) and **MongoDB** (NoSQL database) to store patient and tumor data. The API is built using **FastAPI**, and the prediction system uses a pre-trained machine learning model to classify tumors as **Malignant** or **Benign**.

The purpose of this assignment is to:
1. Design and implement a robust database system for storing breast cancer data.
2. Develop an API to perform CRUD (Create, Read, Update, Delete) operations on the database.
3. Build a prediction system that uses machine learning to classify tumors based on their characteristics.

---

## Database Design and Implementation

### Entity Relationship Diagram (ERD)
The Entity Relationship Diagram (ERD) for the database schema can be viewed [here](https://github.com/M-Pascal/ml_formative_database/blob/main/ERD/Entity_Relational_Diagram.png).

### Step 1: Running the SQL Schema
To set up the MySQL database, run the `sqlSchema.sql` file. This script creates the required tables and sets up the database schema.

```bash
mysql -u root -p < sqlSchema.sql
```
## Database Schema
The database schema consists of the following tables:
- Patients: Stores patient details (e.g., id, diagnosis, created_at).

- Tumor_Mean: Stores mean tumor characteristics (e.g., radius_mean, texture_mean, perimeter_mean).

- Tumor_SE: Stores standard error tumor characteristics.

- Tumor_Worst: Stores worst tumor characteristics.

- Patient_Changes_Log: Logs changes to patient diagnoses (e.g., log_id, patient_id, old_diagnosis, new_diagnosis, change_timestamp).

- Stored Procedures and Triggers
Stored Procedure: InsertOrUpdatePatient - Automates the insertion or updating of patient data.

- Trigger: trigger_log_diagnosis_change - Logs changes to the diagnosis column in the Patients table.

### **Step 2:** Data Cleaning
Before inserting data into the database, the following data cleaning steps are applied:

Column Names: Renamed for consistency (e.g., concave points_mean → concave_points_mean).

Missing Values: Filled with the column mean.

Diagnosis Conversion: Converted to binary values (1 for Malignant, 0 for Benign).

### **Step 3:** MySQL Setup
Log in to MySQL as the root user:

```bash
mysql -u root -p
```
Check if the database and tables were created successfully:
```bash
SHOW DATABASES;
USE breast_cancer_db;
SHOW TABLES;
```
## **Step 4:** MongoDB Setup
The MongoDB database used is breast_cancer_db, which contains the following collections:

- patients: Stores patient details (e.g., id, diagnosis).

- tumor_data: Stores tumor characteristics (e.g., radius_mean, texture_mean).

- diagnosis_logs: Logs changes to patient diagnoses.

Data Insertion
Data is inserted into MongoDB using insert_many():
```bash
patients_collection.insert_many(patients_data_dict)
```
## The API - Task 2
This is a FastAPI-based application for managing patient data and tumor characteristics. It provides endpoints for creating, reading, updating, and deleting records.

FastAPI hosted on render:
> [https://ml-formative-database.onrender.com/docs](https://ml-formative-database.onrender.com/docs)

### Features
Patient Management:
- Create, read, update, and delete patient records.
- Store patient id, diagnosis, and created_at timestamp.

Tumor Data Management:
- Create, read, update, and delete tumor data records.
- Store tumor characteristics (e.g., radius_mean, texture_mean, perimeter_mean).

Diagnosis Logs:
- Retrieve logs of changes to patient diagnoses.

Endpoints
Patient Endpoints
- POST /patients/: Create a new patient.
- GET /patients/: Retrieve all patients.
- GET /patients/{patient_id}: Retrieve a specific patient by ID.
- PUT /patients/{patient_id}: Update a patient by ID.
- DELETE /patients/{patient_id}: Delete a patient by ID.

Tumor Data Endpoints
- POST /tumor_data/: Create new tumor data.
- GET /tumor_data/: Retrieve all tumor data.
- GET /tumor_data/{tumor_id}: Retrieve specific tumor data by ID.
- PUT /tumor_data/{tumor_id}: Update tumor data by ID.
- DELETE /tumor_data/{tumor_id}: Delete tumor data by ID.

Diagnosis Logs Endpoints
- GET /diagnosis_logs/: Retrieve all diagnosis logs.

### Breast Cancer Prediction System - Task 3
This system trains a machine learning model to predict breast cancer diagnosis (malignant or benign) and offers multiple ways to use it:

- **Direct Prediction:** Use the model directly with CSV data.
- **API-Based Prediction:** Fetch data from the API and make predictions.
- **Test Server:** For demonstrations without a database.

Prediction Endpoints
- POST /predict: Predict diagnosis based on input data.
- GET /predict-latest: Predict diagnosis for the latest patient in the database.

### Fetch and Predict Script
The fetch_predict.py script fetches the latest patient data from the API, preprocesses it, and uses the pre-trained model to make a prediction.
```bash
python fetch_predict.py
```
### How to Run the Project
Clone the Repository
```bash
git clone https://github.com/M-Pascal/ml_formative_database.git
```
Install Dependencies
```bash
pip install -r requirements.txt
```
Run the FastAPI Application
```bash
uvicorn main:app --reload
```
Access the API Documentation
Open your browser and navigate to:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Task Distribution
>   - **Task 1 (Database Design and SQL Implementation & MongoDB Implementation):** Pascal Mugisha
>    - **Task 2 (API Development):** Jean Chrisostome Dufitumukiza
>    - **Task 3 (Fetch and Prediction):** Ruth Ishimwe

## Purpose of the Assignment
The purpose of this assignment is to:

- Demonstrate the ability to design and implement a relational and NoSQL database system.
- Develop a RESTful API for managing patient and tumor data.
- Build a machine learning-based prediction system to classify tumors as malignant or benign.
- Integrate all components into a cohesive system that can be used for real-world applications.

### **Done By:**
>   - Pascal Mugisha
>    - Jean Chrisostome Dufitumukiza
>   - Ruth Iradukunda
