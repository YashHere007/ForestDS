from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the updated model and scaler
try:
    model = joblib.load('forest_fire_model_adjusted.pkl')
    scaler = joblib.load('scaler_adjusted.pkl')
except FileNotFoundError:
    raise FileNotFoundError("Model or scaler file not found. Ensure 'forest_fire_model_adjusted.pkl' and 'scaler_adjusted.pkl' are in the project directory.")

# Define top features used by the model
top_features = ['FWI', 'FFMC', 'ISI', 'RH', 'Temperature', 'FFMC_ISI', 'RH_Rain', 'FWI_RH']

# Define feature ranges for validation (aligned with training script)
feature_ranges = {
    'Temperature': (22.0, 42.0),
    'RH': (21.0, 90.0),
    'Ws': (6.0, 29.0),
    'Rain': (0.0, 16.8),
    'FFMC': (28.6, 96.0),
    'DMC': (0.7, 65.9),
    'DC': (6.9, 220.4),
    'ISI': (0.0, 19.0),
    'BUI': (1.1, 68.0),
    'FWI': (0.0, 31.1)
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from request
        data = request.get_json()
        
        # Validate input features
        input_data = {}
        for feature in feature_ranges:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            try:
                value = float(data[feature])
                min_val, max_val = feature_ranges[feature]
                if not (min_val <= value <= max_val):
                    return jsonify({'error': f'{feature} value {value} out of range [{min_val}, {max_val}]'}), 400
                input_data[feature] = value
            except ValueError:
                return jsonify({'error': f'Invalid value for {feature}: {data[feature]}'}), 400
        
        # Compute engineered features
        input_data['FFMC_ISI'] = input_data['FFMC'] * input_data['ISI']
        input_data['RH_Rain'] = input_data['RH'] * input_data['Rain']
        input_data['FWI_RH'] = input_data['FWI'] / (input_data['RH'] + 1e-6)
        
        # Create DataFrame with top features
        input_df = pd.DataFrame([input_data])[top_features]
        
        # Scale inputs
        input_scaled = scaler.transform(input_df)
        
        # Predict
        probability = model.predict_proba(input_scaled)[0][1]
        prediction = 1 if probability >= 0.3 else 0
        result = 'Fire' if prediction == 1 else 'Not Fire'
        
        # Return response
        return jsonify({
            'prediction': result,
            'fire_probability': float(probability),
            'message': 'Prediction successful'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)