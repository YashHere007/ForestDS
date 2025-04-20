Forest Fire Prediction
A web application to predict forest fire risk using a machine learning model trained on the Algerian Forest Fires Dataset and synthetic edge cases.
Features

Predicts Fire/Not Fire based on 10 meteorological and fire weather inputs.
Achieves ~95-97% accuracy with a custom threshold (0.3) for sensitivity.
Handles edge cases (e.g., Temperature=30°C, RH=75%, Rain=1mm, FWI=5).
Simple web interface for user inputs and real-time predictions.

Installation

Clone the repository:
git clone https://github.com/yourusername/forest-fire-prediction.git
cd forest-fire-prediction


Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Ensure forest_fire_model_efficient_fixed.pkl and scaler_efficient_fixed.pkl are in the root directory.

Run the Flask app:
python app.py


Open http://localhost:5000 in your browser.


Usage

Enter values for Temperature, RH, Ws, Rain, FFMC, DMC, DC, ISI, BUI, and FWI within the specified ranges.
Click "Predict" to see the fire risk (Fire/Not Fire) and probability.

Project Structure

app.py: Flask backend API.
templates/index.html: Frontend HTML.
static/styles.css: CSS styling.
static/script.js: JavaScript for API calls.
forest_fire_model_efficient_fixed.pkl: Trained XGBoost model.
scaler_efficient_fixed.pkl: Scaler for input preprocessing.
requirements.txt: Python dependencies.
README.md: Project documentation.

Model Details

Trained on 342 samples (242 original, 100 synthetic edge cases).
Uses 8 features: FWI, FFMC, ISI, RH, Temperature, FFMC_ISI, RH_Rain, FWI_RH.
Optimized with RandomizedSearchCV for efficiency.
Correctly predicts edge cases with ~0.94-0.96 recall for Fire.

License
MIT License
