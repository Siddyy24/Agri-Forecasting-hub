🌾 Agricultural Yield Forecasting System

This project predicts crop yield using machine learning based on soil nutrient levels and weather conditions. It also provides smart recommendations like irrigation advice, crop cycle suggestions, and weather risk assessments to assist farmers and agricultural planners.

📌 Features
✅ Predict crop yield using soil NPK & pH + temperature, rainfall, humidity<br>
✅ Dynamic dashboard with form inputs and visual feedback<br>
✅ Mock/Real-time weather API integration<br>
✅ Soil health assessment & fertilizer suggestions<br>
✅ Crop cycle and irrigation recommendations<br>
✅ Modular Python architecture with Flask API<br>

Project Architecture
Frontend (HTML/JS) ⟶ Flask Backend (app.py) ⟶ Model (forecast_model.py) ⟶ Data Sources (CSV/API)

Folder Structure

project/
│
├── app.py # Flask backend<br>
├── forecast_model.py # ML model training & prediction<br>
├── utils.py # Agriculture logic & helper functions<br>
├── weather_api.py # Mock/real-time weather integration<br>
├── templates/<br>
│ └── index.html # Frontend UI<br>
├── data/<br>
│ └── state_soil_data.csv # Soil dataset<br>
├── static/ (optional) # For CSS or JS<br>
├── requirements.txt # Python dependencies<br>
└── README.md # This file<br>

 Technologies Used
Python (Flask)<br><br>
HTML/CSS/JavaScript (Vanilla)<br>
scikit-learn, pandas, numpy<br>
Weather API (optional)<br>
Bootstrap (optional for UI)<br>

 Model Info
Type: Regression (RandomForest, Linear)<br>
Input Features: N, P, K, pH, avg_temp_c, rainfall, humidity<br>
Output: Predicted crop yield (in units per hectare)<br>

 Setup Instructions
Clone the repository:<br>
git clone https://github.com/your-username/agri-yield-predictor.git<br>
cd agri-yield-predictor<br>
Create a virtual environment (optional but recommended):<br>
python -m venv venv<br>
source venv/bin/activate # On Windows: venv\Scripts\activate<br>
Install dependencies:<br>
pip install -r requirements.txt<br>
Train the model (if model.pkl doesn’t exist):<br>
python forecast_model.py<br>
Run the Flask app:<br>
python app.py<br>
Open in browser:<br>
Visit http://localhost:5000<br>

API Notes<br>
If using OpenWeather API:<br>
Set the API key in your environment: export OPENWEATHER_API_KEY=your_key<br>
Or update directly in weather_api.py (not recommended for production)

Sample Prediction
Input:<br>
{
"state": "Punjab",<br>
"N": 180,<br>
"P": 45,<br>
"K": 200,<br>
"pH": 6.8,<br>
"avg_temp_c": 26.5,<br>
"total_rainfall_mm": 950,<br>
"avg_humidity_percent": 60<br>
}<br>
Output:<br>

{<br>
"prediction": 3225.0,<br>
"yield_category": "Good Yield",<br>
"irrigation": "⚠️ Monitor closely: 31.7 mm rainfall (barely sufficient)",<br>
"crop_cycle": "🌾 Rice/Maize → Plant in Jun-Jul, Harvest in Oct-Nov",<br>
"soil_health": {...},<br>
"weather_risks": {...}<br>
}<br>

 Future Scope:<br>
    Integrate real-time weather APIs<br>
    Visualize predictions and trends<br>
    Mobile app version for farmers<br>
    Multi-language support<br>
    Crop recommendation system<br>

 License
This project is licensed under the MIT License — feel free to use or modify with credit.


 Contributions<br>
Aarohi Shinde-Aarohicodes<br>
Swami Lande-swamilande<br>
Siddhi Belekar-Siddy24<br>
Akash wagh-akshawagh07<br>

