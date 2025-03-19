import requests
import pickle
import pandas as pd

# API URL for fetching the latest patient entry
API_URL = "http://127.0.0.1:8000/patients/last"

# Path to the saved model
MODEL_PATH = "./saved_best_model/logistic_regression.pkl"

# Fetch the latest patient data from the API
def fetch_latest_patient():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")

# Preprocess the data for prediction
def preprocess_data(patient_data):
    # Extract relevant features from the JSON response
    tumor_mean = patient_data.get("tumor_mean", {})
    tumor_se = patient_data.get("tumor_se", {})
    tumor_worst = patient_data.get("tumor_worst", {})
    
    # Combine selected features into a single list following model training format
    features = [
        tumor_mean.get("radius_mean", 0),
        tumor_mean.get("texture_mean", 0),
        tumor_mean.get("perimeter_mean", 0),
        tumor_mean.get("area_mean", 0),
        tumor_mean.get("smoothness_mean", 0),
        tumor_mean.get("compactness_mean", 0),
        tumor_mean.get("concavity_mean", 0),
        tumor_mean.get("concave_points_mean", 0),
        tumor_mean.get("symmetry_mean", 0),
        tumor_mean.get("fractal_dimension_mean", 0),
        tumor_se.get("radius_se", 0),
        tumor_se.get("texture_se", 0),
        tumor_se.get("perimeter_se", 0),
        tumor_se.get("area_se", 0),
        tumor_se.get("smoothness_se", 0),
        tumor_se.get("compactness_se", 0),
        tumor_se.get("concavity_se", 0),
        tumor_se.get("concave_points_se", 0),
        tumor_se.get("symmetry_se", 0),
        tumor_se.get("fractal_dimension_se", 0),
        tumor_worst.get("radius_worst", 0),
        tumor_worst.get("texture_worst", 0),
        tumor_worst.get("perimeter_worst", 0),
        tumor_worst.get("area_worst", 0),
        tumor_worst.get("smoothness_worst", 0),
        tumor_worst.get("compactness_worst", 0),
        tumor_worst.get("concavity_worst", 0),
        tumor_worst.get("concave_points_worst", 0),
        tumor_worst.get("symmetry_worst", 0),
        tumor_worst.get("fractal_dimension_worst", 0),
    ]
    
    # Create DataFrame
    df = pd.DataFrame([features], columns=[
        "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
        "smoothness_mean", "compactness_mean", "concavity_mean", "concave_points_mean",
        "symmetry_mean", "fractal_dimension_mean", "radius_se", "texture_se", "perimeter_se", "area_se",
        "smoothness_se", "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
        "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst", "compactness_worst",
        "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
    ])
    
    # Convert DataFrame to NumPy array (remove feature names)
    return df.to_numpy()

# Load the trained model and make a prediction
def predict(data):
    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)
        prediction = model.predict(data)
        return "Malignant" if prediction[0] == 1 else "Benign"
    except Exception as e:
        raise Exception(f"Error loading or predicting with the model: {e}")

if __name__ == "__main__":
    try:
        print("Fetching latest patient data...")
        patient_data = fetch_latest_patient()
        print("Patient data retrieved successfully.")
        
        print("Preprocessing data for prediction...")
        processed_data = preprocess_data(patient_data)
        
        # Debugging: Print the shape and content of the processed data
        print("Processed Data Shape:", processed_data.shape)
        print("Processed Data Content:", processed_data)
        
        print("Making prediction...")
        result = predict(processed_data)
        print(f"Predicted Diagnosis: {result}")
    except Exception as e:
        print(f"Error: {e}")
