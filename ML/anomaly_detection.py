# anomaly_detection.py

from sklearn.base import BaseEstimator
import logging
from joblib import load
import numpy as np


def load_model(model_path='saved_model.pkl'):
    try:
        model = load(model_path)
        return model
    except FileNotFoundError:
        print(f"Error: Model file '{model_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def predict_anomaly(features, model):
    # Input validation
    if not isinstance(features, (list, np.ndarray)):
        raise ValueError("Features must be a list or array-like object.")
    if not isinstance(model, BaseEstimator):
        raise ValueError("Model must be a trained model.")

    try:
        # Make a prediction
        prediction = model.predict([features])
        return prediction[0]
    except Exception as e:
        # Log the error message
        logging.error(f"Error predicting anomaly: {e}")
        # Raise a custom exception
        raise RuntimeError(
            "An error occurred while predicting anomaly.") from e
