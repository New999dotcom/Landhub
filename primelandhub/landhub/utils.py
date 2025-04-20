import joblib
import numpy as np
import pandas as pd

# ✅ Load the trained model
model = joblib.load('property_price_model.joblib')

def predict_price(property_data):
    # ✅ Convert Data to DataFrame for Model Processing
    df = pd.DataFrame([property_data])

    # ✅ Ensure Correct Data Types
    df['bedrooms'] = df['bedrooms'].astype(int)
    df['bathrooms'] = df['bathrooms'].astype(int)
    df['area_sqft'] = df['area_sqft'].astype(float)
    df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    df['price_per_sqft'] = df['price_per_sqft'].astype(float)

    # ✅ Make Prediction
    predicted_price_log = model.predict(df)

    # ✅ Reverse Log Transformation
    predicted_price = np.expm1(predicted_price_log)[0]

    return round(predicted_price, 2)
