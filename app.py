import os
import sys

import joblib
import pandas as pd
from flask import Flask, jsonify, request

from src.config.configuration import ALL_SELECTED_FEATURES

# Ensure the `src` module is in the `PYTHONPATH`
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

app = Flask(__name__)

# Load the model
pipeline = joblib.load("rental_price_model.pkl")


@app.route("/predict", methods=["POST"])
def predict():
    # Get the data from the request
    data = request.json

    # Convert data to DataFrame
    df = pd.DataFrame([data])

    # Predict using the loaded model
    prediction = pipeline.predict(df[ALL_SELECTED_FEATURES])

    # Return the prediction
    return jsonify({"predicted_rent": float(prediction[0])})


if __name__ == "__main__":
    app.run(debug=False, port=5000)
