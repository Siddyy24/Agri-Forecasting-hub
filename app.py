from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from forecast_model import AgriYieldForecaster
from weather_api import get_current_weather
import os
# near other imports
from utils import (
    get_irrigation_recommendation,
    suggest_crop_cycle,
    format_prediction_summary,
    generate_farming_tips,
    validate_input_parameters
)


app = Flask(__name__)

# Initialize the forecaster
forecaster = AgriYieldForecaster()

# Load the trained model on startup
model_loaded = False
try:
    if forecaster.load_model():
        model_loaded = True
        print("Model loaded successfully!")
    else:
        print("No trained model found. Please run forecast_model.py first to train the model.")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_yield():
    """Predict crop yield and return recommendations."""
    try:
        if not model_loaded:
            return jsonify({'error': 'Model not loaded. Please train the model first.', 'success': False})

        data = request.json or {}
        
        # Validate required fields quickly (use your util validation)
        validation = validate_input_parameters(data)
        if not validation['success']:
            return jsonify({'error': 'Invalid input', 'details': validation['errors'], 'success': False})

        # Build input_data dict (ensure numeric types)
        input_data = {
            'state': data.get('state', ''),
            'N': float(data.get('N', 0)),
            'P': float(data.get('P', 0)),
            'K': float(data.get('K', 0)),
            'pH': float(data.get('pH', 7)),
            'avg_temp_c': float(data.get('avg_temp_c', 25)),
            'total_rainfall_mm': float(data.get('total_rainfall_mm', 0)),
            'avg_humidity_percent': float(data.get('avg_humidity_percent', 50))
        }
        if 'year' in data:
            input_data['year'] = int(data['year'])

        # Predict
        prediction_raw = forecaster.predict(input_data)
        prediction = round(float(prediction_raw), 2)

        # Create the formatted summary (uses utils)
        summary = format_prediction_summary(prediction, input_data)

        # Farming tips (friendly list)
        farming_tips = generate_farming_tips(
            {'N': input_data['N'], 'P': input_data['P'], 'K': input_data['K'], 'pH': input_data['pH']},
            {'avg_temp_c': input_data['avg_temp_c'], 'total_rainfall_mm': input_data['total_rainfall_mm'], 'avg_humidity_percent': input_data['avg_humidity_percent']}
        )

        # Return structured response (friendly for frontend)
        return jsonify({
            'success': True,
            'prediction': prediction,
            'yield_category': summary.get('yield_category'),
            'irrigation': summary.get('irrigation_advice'),
            'crop_cycle': summary.get('crop_cycle'),
            'soil_health': summary.get('soil_health'),
            'weather_risks': summary.get('weather_risks'),
            'farming_tips': farming_tips
        })

    except ValueError as e:
        return jsonify({'error': f'Invalid input data: {str(e)}', 'success': False})
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}', 'success': False})


@app.route('/weather/<state>')
def get_weather_data(state):
    """Get weather data for a specific state"""
    try:
        weather_data = get_current_weather(state)
        return jsonify({
            'weather_data': weather_data,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Weather data error: {str(e)}',
            'success': False
        })

@app.route('/states')
def get_states():
    """Get list of available states"""
    try:
        # Read soil data to get available states
        soil_data = pd.read_csv('data/state_soil_data.csv')
        states = sorted(soil_data['state'].unique().tolist())
        return jsonify({
            'states': states,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Error loading states: {str(e)}',
            'success': False
        })

@app.route('/soil-data/<state>')
def get_soil_data(state):
    """Get soil data for a specific state"""
    try:
        soil_data = pd.read_csv('data/state_soil_data.csv')
        state_soil = soil_data[soil_data['state'] == state]
        
        if state_soil.empty:
            return jsonify({
                'error': f'No soil data found for state: {state}',
                'success': False
            })
        
        soil_info = {
            'N': float(state_soil['N'].iloc[0]),
            'P': float(state_soil['P'].iloc[0]),
            'K': float(state_soil['K'].iloc[0]),
            'pH': float(state_soil['pH'].iloc[0])
        }
        
        return jsonify({
            'soil_data': soil_info,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error loading soil data: {str(e)}',
            'success': False
        })

@app.route('/model-info')
def get_model_info():
    """Get information about the loaded model"""
    try:
        if not model_loaded:
            return jsonify({
                'error': 'No model loaded',
                'success': False
            })
        
        model_info = {
            'model_type': type(forecaster.model).__name__,
            'features': forecaster.feature_columns,
            'model_loaded': model_loaded
        }
        
        return jsonify({
            'model_info': model_info,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error getting model info: {str(e)}',
            'success': False
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'success': True
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'success': False
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500

if __name__ == '__main__':
    # Check if model exists, if not, suggest training
    if not model_loaded:
        print("\n" + "="*60)
        print("WARNING: No trained model found!")
        print("Please run the following command to train the model:")
        print("python forecast_model.py")
        print("="*60 + "\n")
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)