import requests
import pickle
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API endpoint to fetch the latest entry
API_URL = "https://ml-formative-database.onrender.com/patients"

# Path to the trained model
MODEL_PATH = "../saved_best_model/Logistic_regression.pkl"

def fetch_latest_entry():
    """Fetch the latest data entry from the API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()

        if not data:
            logging.warning("No data received from the API.")
            return None
        
        logging.info(f"Fetched latest entry: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def load_model():
    """Load the trained model from a pickle file."""
    try:
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
        logging.info("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def preprocess_data(data):
    """Handle missing values and encode categorical features."""
    try:
        df = pd.DataFrame([data])  # Convert dictionary to DataFrame

        # Handle missing values
        for col in df.columns:
            if df[col].dtype == "object":  # Categorical feature
                df[col].fillna(df[col].mode()[0], inplace=True)
            else:  # Numerical feature
                df[col].fillna(df[col].median(), inplace=True)

        # One-hot encoding for categorical features
        df = pd.get_dummies(df)

        logging.info("Data preprocessing completed.")
        return df
    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        return None

def prepare_and_predict(data, model):
    """Prepare input data and make predictions."""
    try:
        processed_data = preprocess_data(data)
        if processed_data is None:
            logging.error("Error in data processing.")
            return None

        # Ensure input features match model's training data
        prediction = model.predict(processed_data)
        
        logging.info(f"Prediction: {prediction}")
        return prediction
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return None

def main():
    latest_data = fetch_latest_entry()
    if latest_data is None:
        logging.error("Failed to fetch data.")
        return

    model = load_model()
    if model is None:
        logging.error("Failed to load model.")
        return

    prepare_and_predict(latest_data, model)

if __name__ == "__main__":
    main()
