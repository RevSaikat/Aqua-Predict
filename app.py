from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import numpy as np
import datetime
import joblib  # Changed from pickle to joblib for model loading
import os
import logging
from config import config

# Initialize Flask app
app = Flask(__name__, template_folder="template")

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
CORS(app)
csrf = CSRFProtect(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model with error handling
model_path = app.config['MODEL_PATH']
try:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    model = joblib.load(model_path)  # Changed from pickle.load
    logger.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    model = None


def validate_input(data):
    """Validate form input data"""
    errors = []
    
    # Required fields
    required_fields = [
        'date', 'mintemp', 'maxtemp', 'rainfall', 'evaporation', 'sunshine',
        'windgustspeed', 'windspeed9am', 'windspeed3pm', 'humidity9am', 'humidity3pm',
        'pressure9am', 'pressure3pm', 'temp9am', 'temp3pm', 'cloud9am', 'cloud3pm',
        'location', 'winddir9am', 'winddir3pm', 'windgustdir', 'raintoday'
    ]
    
    
    for field in required_fields:
        if field not in data or data[field] == '':
            # Provide more user-friendly field names
            field_names = {
                'location': 'Location',
                'winddir9am': 'Wind Direction at 9am',
                'winddir3pm': 'Wind Direction at 3pm',
                'windgustdir': 'Wind Gust Direction',
                'raintoday': 'Rain Today'
            }
            friendly_name = field_names.get(field, field.replace('_', ' ').title())
            errors.append(f"Please select/enter a value for '{friendly_name}'")
    
    if errors:
        return False, errors
    
    
    # Validate ranges
    try:
        min_temp = float(data['mintemp'])
        max_temp = float(data['maxtemp'])
        
        if min_temp < -50 or min_temp > 60:
            errors.append("Minimum temperature must be between -50°C and 60°C")
        if max_temp < -50 or max_temp > 60:
            errors.append("Maximum temperature must be between -50°C and 60°C")
        if min_temp > max_temp:
            errors.append("Minimum temperature cannot be greater than maximum temperature")
        
        # Validate humidity (0-100%)
        humidity_9am = float(data['humidity9am'])
        humidity_3pm = float(data['humidity3pm'])
        if not (0 <= humidity_9am <= 100):
            errors.append("Humidity at 9am must be between 0% and 100%")
        if not (0 <= humidity_3pm <= 100):
            errors.append("Humidity at 3pm must be between 0% and 100%")
        
        # Validate rainfall (non-negative)
        rainfall = float(data['rainfall'])
        if rainfall < 0:
            errors.append("Rainfall cannot be negative")
        
        # Validate wind speeds (non-negative)
        if float(data['windgustspeed']) < 0:
            errors.append("Wind gust speed cannot be negative")
        if float(data['windspeed9am']) < 0:
            errors.append("Wind speed at 9am cannot be negative")
        if float(data['windspeed3pm']) < 0:
            errors.append("Wind speed at 3pm cannot be negative")
            
    except ValueError as e:
        errors.append(f"Invalid numeric value: {str(e)}")
    
    if errors:
        return False, errors
    
    return True, None


@app.route("/", methods=['GET'])
def home():
    """Home page route"""
    return render_template("index.html")


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    """Prediction route with comprehensive error handling"""
    if request.method == "GET":
        return render_template("predictor.html")
    
    try:
        global model
        # Ensure model is loaded (fallback for debug reloader)
        if model is None:
            try:
                model_path = app.config['MODEL_PATH']
                model = joblib.load(model_path)  # Changed from pickle.load
                logger.info(f"Model reloaded successfully from {model_path}")
            except Exception as e2:
                logger.error(f"Failed to reload model: {str(e2)}")
                return render_template("error.html", message="Prediction service is currently unavailable. Please try again later."), 503

        # Validate input
        is_valid, errors = validate_input(request.form)
        if not is_valid:
            assert errors is not None  # validate_input guarantees list[str] when is_valid=False
            error_message = "Please fix the following errors:<br>" + "<br>".join(errors)
            return render_template("error.html", message=error_message), 400

        # Extract and process form data
        date = request.form['date']
        day = float(pd.to_datetime(date, format="%Y-%m-%d").day)
        month = float(pd.to_datetime(date, format="%Y-%m-%d").month)

        # Numerical inputs
        minTemp = float(request.form['mintemp'])
        maxTemp = float(request.form['maxtemp'])
        rainfall = float(request.form['rainfall'])
        evaporation = float(request.form['evaporation'])
        sunshine = float(request.form['sunshine'])
        windGustSpeed = float(request.form['windgustspeed'])
        windSpeed9am = float(request.form['windspeed9am'])
        windSpeed3pm = float(request.form['windspeed3pm'])
        humidity9am = float(request.form['humidity9am'])
        humidity3pm = float(request.form['humidity3pm'])
        pressure9am = float(request.form['pressure9am'])
        pressure3pm = float(request.form['pressure3pm'])
        temp9am = float(request.form['temp9am'])
        temp3pm = float(request.form['temp3pm'])
        cloud9am = float(request.form['cloud9am'])
        cloud3pm = float(request.form['cloud3pm'])
        
        # Categorical inputs - validate before conversion
        try:
            location = float(request.form['location'])
            winddDir9am = float(request.form['winddir9am'])
            winddDir3pm = float(request.form['winddir3pm'])
            windGustDir = float(request.form['windgustdir'])
            rainToday = float(request.form['raintoday'])
        except ValueError as e:
            logger.error(f"Invalid dropdown value: {str(e)}")
            return render_template("error.html", message="Please select valid options from all dropdown menus (Location, Wind Directions, Rain Today)."), 400


        # Prepare input array for prediction
        input_lst = [
            location, minTemp, maxTemp, rainfall, evaporation, sunshine,
            windGustDir, windGustSpeed, winddDir9am, winddDir3pm, windSpeed9am, windSpeed3pm,
            humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, 
            temp9am, temp3pm, rainToday, month, day
        ]
        
        # Make prediction
        pred = model.predict([input_lst])
        output = pred[0]
        
        # Log prediction
        logger.info(f"Prediction made: {'Rainy' if output == 1 else 'Sunny'} for date {date}")
        
        # Return result
        if output == 0:
            return render_template("after_sunny.html")
        else:
            return render_template("after_rainy.html")
            
    except ValueError as e:
        logger.error(f"Value error in prediction: {str(e)}")
        return render_template("error.html", message="Invalid input data. Please check your values and try again."), 400
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {str(e)}")
        return render_template("error.html", message="An unexpected error occurred. Please try again later."), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("error.html", message="Page not found."), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template("error.html", message="Internal server error. Please try again later."), 500


if __name__ == '__main__':
    # Run the app
    debug_mode = app.config.get('DEBUG', False)
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
