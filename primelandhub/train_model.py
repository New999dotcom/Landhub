import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# Load Data
data = pd.read_csv('property_listings.csv')  # Updated to match your earlier context

# Ensure Required Columns Exist
data['total_rooms'] = data['bedrooms'] + data['bathrooms']
data['price_per_sqft'] = data['price'] / data['area_sqft']

# Compute location-based price_per_sqft averages
avg_price_per_sqft_by_place = data.groupby('place')['price_per_sqft'].mean().to_dict()

# Define Features & Target
features = ['propertytype', 'prop', 'bedrooms', 'bathrooms', 'area_sqft', 
            'is_furnished', 'parking_space', 'place', 'total_rooms', 'price_per_sqft']
X = data[features].copy()  # Avoid slice issues
y = np.log1p(data['price'])  # Log transform target

# Convert Boolean Values to Categorical Format (Future-Proof)
X['is_furnished'] = X['is_furnished'].astype('object')
X['parking_space'] = X['parking_space'].astype('object')
X.loc[:, 'is_furnished'] = X['is_furnished'].map({True: 'Yes', False: 'No'})
X.loc[:, 'parking_space'] = X['parking_space'].map({True: 'Yes', False: 'No'})

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing Pipeline
categorical_features = ['propertytype', 'prop', 'place', 'is_furnished', 'parking_space']
numerical_features = ['bedrooms', 'bathrooms', 'area_sqft', 'total_rooms', 'price_per_sqft']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', StandardScaler(), numerical_features)
    ])

# Define & Train Model (XGBoost)
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=10, random_state=42))
])

model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))  # Reverse log transformation
r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))

print(f"Improved MAE: {mae:.2f}")
print(f"Improved R²: {r2:.4f}")

# Cross-Validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"Cross-Validated R² Score: {cv_scores.mean():.4f}")

# Save Model and Price per Sqft Averages
joblib.dump(model, 'property_price_model.joblib')
joblib.dump(avg_price_per_sqft_by_place, 'avg_price_per_sqft_by_place.joblib')