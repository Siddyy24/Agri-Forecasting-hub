# Agri-Forecasting Hub 🌾
A Flask-based web application for agricultural forecasting that provides weather predictions, yield forecasting, and irrigation recommendations.

## Features

- *Weather Forecast Integration*: 5-day weather forecast using OpenWeather API
- *Yield Prediction*: Machine learning model for crop yield prediction based on rainfall
- *Irrigation Recommendations*: Smart irrigation advice based on weather forecasts
- *Modern Dashboard*: Clean, responsive web interface with agriculture-themed design

 ## Project Structure
 
 agri_forecast/<br>
├── app.py                 # Main Flask application <br>
├── weather_api.py         # Weather API integration <br>
├── forecast_model.py      # ML model for yield prediction <br>
├── templates/
│   └── index.html         # Dashboard HTML template<br>
├── data/
│   └── sample_yield.csv   # Sample dataset for training<br>
├── requirements.txt       # Python dependencies<br>
└── README.md             # This file<br>

## Installation & Setup

### 1. Install Dependencies

bash
cd agri_forecast
pip install -r requirements.txt

### 2. Set Up OpenWeather API (Optional)

For real weather data, get a free API key from [OpenWeatherMap](https://openweathermap.org/api):
bash
# Set environment variable (Windows)
set OPENWEATHER_API_KEY=your_api_key_here

# Set environment variable (Linux/Mac)
export OPENWEATHER_API_KEY=your_api_key_here

*Note*: The app works with mock data if no API key is provided.
### 3. Run the Application

bash
python app.py
The application will be provided at: http://localhost:5000

## Usage

 ### Dashboard Features
1. *Yield Prediction*: 
   - View predicted yield for 850mm rainfall
   - Use the custom prediction form to test different rainfall values
2. *Irrigation Advice*: 
   - Get smart irrigation recommendations based on weather forecast
   - Recommendations change based on expected rainfall

3. *Weather Forecast*: 
   - View 5-day weather forecast with temperature and rainfall
   - Visual indicators for weather conditions

4. *Model Information*: 
   - View ML model performance metrics
   - R² score, MSE, and model coefficients

  ### API Endpoints

- GET / - Main dashboard
- POST /predict - Yield prediction API
- GET /weather - Weather forecast API
- GET /model-info - Model information API

## Technical Details

  ### Machine Learning Model

- *Algorithm*: Linear Regression
- *Features*: Rainfall (mm)
- *Target*: Crop Yield (kg/hectare)
- *Training Data*: 11 sample records (2020-2030)

  ### Weather Integration

- *Primary*: OpenWeather API (5-day forecast)
- *Fallback*: Mock data for demonstration
- *Data Points*: Temperature, rainfall, conditions

  ### Irrigation Logic

- *Irrigate*: If rainfall < 1mm in next 2 days
- *Skip*: If sufficient rainfall expected

## Customization

  ### Adding More Data

1. Update data/sample_yield.csv with more historical data
2. The model will automatically retrain with new data

### Changing Weather Location
Modify the city and country in app.py:
python
weather_forecast = weather_api.get_weather_forecast("YourCity", "YourCountry")

### Styling
The dashboard uses a green agriculture theme. Modify the CSS in templates/index.html to customize the appearance.

## Troubleshooting
### Common Issues 
1.*Import Errors*.Ensure all dependencies are installed <br>
2.*Data Loading*.Check that data/sample_yield.csv exists <br>
3. *Weather API*: Verify API key is set correctly <br>
4. *Port Issues*: Change port in app.py if 5000 is occupied <br>

### Debug Mode
The application runs in debug mode by default. For production:

python
 app.run(debug=False, host='0.0.0.0', port=5000)

 ## Future Enhancements
- [ ] Multiple crop types support
- [ ] Historical weather data integration
- [ ] Advanced ML models (Random Forest, Neural Networks)
- [ ] User authentication and data persistence
- [ ] Mobile app integration
- [ ] Real-time notifications















