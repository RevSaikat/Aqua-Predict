# AquaPredict API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:5000` (Development)  
**Last Updated:** November 26, 2025

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request/Response Examples](#request-response-examples)
5. [Error Handling](#error-handling)
6. [Field Specifications](#field-specifications)
7. [Integration Guide](#integration-guide)

---

## Overview

AquaPredict is a Flask-based REST API that provides rainfall prediction capabilities using machine learning models. The API accepts meteorological data and returns predictions indicating whether it will rain the next day.

### Key Features
- ✅ Machine learning-powered predictions
- ✅ CSRF protection for forms
- ✅ CORS enabled for cross-origin requests
- ✅ Comprehensive input validation
- ✅ Multiple ML models (CatBoost, XGBoost, SVC, LogReg, Naive Bayes)

### Tech Stack
- **Framework:** Flask 3.0.3
- **ML Libraries:** scikit-learn, CatBoost, XGBoost
- **Data Processing:** pandas, numpy
- **Security:** Flask-WTF (CSRF), Flask-CORS

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

> ⚠️ **Production Note:** Consider implementing API key authentication or OAuth2 for production deployments.

---

## Endpoints

### 1. Home Page

**Endpoint:** `GET /`

Returns the main landing page with information about AquaPredict.

#### Request
```http
GET / HTTP/1.1
Host: localhost:5000
```

#### Response
- **Status Code:** `200 OK`
- **Content-Type:** `text/html`
- **Body:** HTML page with navigation to About, Dashboard, Developer info, and Predictor

---

### 2. Get Prediction Form

**Endpoint:** `GET /predict`

Returns the prediction form page where users can input meteorological data.

#### Request
```http
GET /predict HTTP/1.1
Host: localhost:5000
```

#### Response
- **Status Code:** `200 OK`
- **Content-Type:** `text/html`
- **Body:** HTML form with all required input fields and CSRF token

---

### 3. Make Prediction

**Endpoint:** `POST /predict`

Submits meteorological data to get a rainfall prediction.

#### Request Headers
```http
POST /predict HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded
```

#### Request Body (Form Data)

| Field | Type | Required | Description | Example | Range/Options |
|-------|------|----------|-------------|---------|---------------|
| `csrf_token` | string | Yes | CSRF protection token | Auto-generated | - |
| `date` | date | Yes | Prediction date | 2025-11-26 | YYYY-MM-DD |
| `mintemp` | float | Yes | Minimum temperature (°C) | 13.4 | -10 to 40 |
| `maxtemp` | float | Yes | Maximum temperature (°C) | 22.9 | -5 to 50 |
| `rainfall` | float | Yes | Rainfall (mm) | 0.0 | 0 to 500 |
| `evaporation` | float | Yes | Evaporation (mm) | 4.8 | 0 to 100 |
| `sunshine` | float | Yes | Sunshine hours | 8.5 | 0 to 24 |
| `windgustspeed` | float | Yes | Wind gust speed (km/h) | 44 | 0 to 200 |
| `windspeed9am` | float | Yes | Wind speed at 9am (km/h) | 20 | 0 to 150 |
| `windspeed3pm` | float | Yes | Wind speed at 3pm (km/h) | 24 | 0 to 150 |
| `humidity9am` | float | Yes | Humidity at 9am (%) | 71 | 0 to 100 |
| `humidity3pm` | float | Yes | Humidity at 3pm (%) | 22 | 0 to 100 |
| `pressure9am` | float | Yes | Pressure at 9am (hPa) | 1007.7 | 900 to 1100 |
| `pressure3pm` | float | Yes | Pressure at 3pm (hPa) | 1007.1 | 900 to 1100 |
| `temp9am` | float | Yes | Temperature at 9am (°C) | 16.9 | -10 to 50 |
| `temp3pm` | float | Yes | Temperature at 3pm (°C) | 21.8 | -10 to 50 |
| `cloud9am` | integer | Yes | Cloud cover at 9am (oktas) | 8 | 0 to 8 |
| `cloud3pm` | integer | Yes | Cloud cover at 3pm (oktas) | 8 | 0 to 8 |
| `location` | integer | Yes | Location code | 10 | See Location Codes |
| `winddir9am` | integer | Yes | Wind direction at 9am | 1 | See Wind Direction Codes |
| `winddir3pm` | integer | Yes | Wind direction at 3pm | 2 | See Wind Direction Codes |
| `windgustdir` | integer | Yes | Wind gust direction | 3 | See Wind Direction Codes |
| `raintoday` | integer | Yes | Did it rain today? | 1 | 0=No, 1=Yes |

#### Response (Success - No Rain Expected)
- **Status Code:** `200 OK`
- **Content-Type:** `text/html`
- **Body:** `after_sunny.html` page indicating no rain expected

#### Response (Success - Rain Expected)
- **Status Code:** `200 OK`
- **Content-Type:** `text/html`
- **Body:** `after_rainy.html` page indicating rain expected

#### Response (Validation Error)
- **Status Code:** `400 Bad Request`
- **Content-Type:** `text/html`
- **Body:** `error.html` page with specific error messages

#### Response (Server Error)
- **Status Code:** `500 Internal Server Error`
- **Content-Type:** `text/html`
- **Body:** `error.html` page with generic error message

---

## Request/Response Examples

### Example 1: Successful Prediction (cURL)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrf_token=YOUR_CSRF_TOKEN" \
  --data "date=2025-11-26" \
  --data "mintemp=13.4" \
  --data "maxtemp=22.9" \
  --data "rainfall=0.0" \
  --data "evaporation=4.8" \
  --data "sunshine=8.5" \
  --data "windgustspeed=44" \
  --data "windspeed9am=20" \
  --data "windspeed3pm=24" \
  --data "humidity9am=71" \
  --data "humidity3pm=22" \
  --data "pressure9am=1007.7" \
  --data "pressure3pm=1007.1" \
  --data "temp9am=16.9" \
  --data "temp3pm=21.8" \
  --data "cloud9am=8" \
  --data "cloud3pm=8" \
  --data "location=10" \
  --data "winddir9am=1" \
  --data "winddir3pm=2" \
  --data "windgustdir=3" \
  --data "raintoday=1"
```

### Example 2: Python Integration

```python
import requests

# Get CSRF token first
session = requests.Session()
response = session.get('http://localhost:5000/predict')
# Extract CSRF token from HTML (you'll need to parse the HTML or use a library like BeautifulSoup)

# Make prediction
data = {
    'csrf_token': 'YOUR_CSRF_TOKEN',  # Extract from form
    'date': '2025-11-26',
    'mintemp': 13.4,
    'maxtemp': 22.9,
    'rainfall': 0.0,
    'evaporation': 4.8,
    'sunshine': 8.5,
    'windgustspeed': 44,
    'windspeed9am': 20,
    'windspeed3pm': 24,
    'humidity9am': 71,
    'humidity3pm': 22,
    'pressure9am': 1007.7,
    'pressure3pm': 1007.1,
    'temp9am': 16.9,
    'temp3pm': 21.8,
    'cloud9am': 8,
    'cloud3pm': 8,
    'location': 10,  # Sydney
    'winddir9am': 1,  # N
    'winddir3pm': 2,  # N
    'windgustdir': 3,  # N
    'raintoday': 1   # Yes
}

response = session.post('http://localhost:5000/predict', data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
```

### Example 3: JavaScript/AJAX Integration

```javascript
// First, get the CSRF token from the form
const csrfToken = document.querySelector('input[name="csrf_token"]').value;

// Prepare form data
const formData = new FormData();
formData.append('csrf_token', csrfToken);
formData.append('date', '2025-11-26');
formData.append('mintemp', '13.4');
formData.append('maxtemp', '22.9');
formData.append('rainfall', '0.0');
formData.append('evaporation', '4.8');
formData.append('sunshine', '8.5');
formData.append('windgustspeed', '44');
formData.append('windspeed9am', '20');
formData.append('windspeed3pm', '24');
formData.append('humidity9am', '71');
formData.append('humidity3pm', '22');
formData.append('pressure9am', '1007.7');
formData.append('pressure3pm', '1007.1');
formData.append('temp9am', '16.9');
formData.append('temp3pm', '21.8');
formData.append('cloud9am', '8');
formData.append('cloud3pm', '8');
formData.append('location', '10');
formData.append('winddir9am', '1');
formData.append('winddir3pm', '2');
formData.append('windgustdir', '3');
formData.append('raintoday', '1');

// Make request
fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData,
    credentials: 'same-origin'  // Important for CSRF
})
.then(response => response.text())
.then(html => {
    console.log('Prediction result:', html);
})
.catch(error => {
    console.error('Error:', error);
});
```

---

## Error Handling

### Validation Errors (400)

The API validates all input data. Common validation errors include:

| Error | Description |
|-------|-------------|
| Missing required field | One or more required fields are empty |
| Temperature range error | Min/max temperature outside valid range (-50°C to 60°C) |
| Humidity range error | Humidity not between 0% and 100% |
| Negative values | Rainfall or wind speeds cannot be negative |
| Min > Max temperature | Minimum temperature exceeds maximum temperature |
| Invalid dropdown | Location or wind direction not selected |

**Example Error Response:**
```html
<!-- error.html page with message -->
<div class="error-message">
  Please fix the following errors:<br>
  - Minimum temperature must be between -50°C and 60°C<br>
  - Humidity at 9am must be between 0% and 100%
</div>
```

### Server Errors (500, 503)

| Status Code | Description |
|-------------|-------------|
| 503 Service Unavailable | Model file not found or failed to load |
| 500 Internal Server Error | Unexpected error during prediction |

---

## Field Specifications

### Location Codes

| Code | Location | Code | Location | Code | Location |
|------|----------|------|----------|------|----------|
| 1 | Portland | 18 | Watsonia | 35 | Perth Airport |
| 2 | Cairns | 19 | Newcastle | 36 | Bendigo |
| 3 | Walpole | 20 | Wollongong | 37 | Richmond |
| 4 | Dartmoor | 21 | Brisbane | 38 | WaggaWagga |
| 5 | MountGambier | 22 | William Town | 39 | Townsville |
| 6 | NorfolkIsland | 23 | Launceston | 40 | PearceRAAF |
| 7 | Albany | 24 | Adelaide | 41 | Salmon Gums |
| 8 | Witchcliffe | 25 | Melbourne Airport | 42 | Moree |
| 9 | CoffsHarbour | 26 | Perth | 43 | Cobar |
| 10 | Sydney | 27 | Sale | 44 | Mildura |
| 11 | Darwin | 28 | Melbourne | 45 | Katherine |
| 12 | MountGinini | 29 | - | 46 | AliceSprings |
| 13 | NorahHead | 30 | Albury | 47 | Nhil |
| 14 | Ballarat | 31 | Penrith | 48 | Woomera |
| 15 | GoldCoast | 32 | Nuriootpa | 49 | Uluru |
| 16 | Sydney Airport | 33 | BadgerysCreek | - | - |
| 17 | Hobart | 34 | Tuggeranong | - | - |

### Wind Direction Codes (9am)

| Code | Direction |
|------|-----------|
| 0 | NNW |
| 1 | N |
| 2 | NW |
| 3 | NNE |
| 4 | WNW |
| 5 | W |
| 6 | WSW |
| 7 | SW |
| 8 | SSW |
| 9 | NE |
| 10 | S |
| 11 | SSE |
| 12 | ENE |
| 13 | SE |
| 14 | ESE |
| 15 | E |

### Wind Direction Codes (3pm)

| Code | Direction |
|------|-----------|
| 0 | NW |
| 1 | NNW |
| 2 | N |
| 3 | WNW |
| 4 | W |
| 5 | NNE |
| 6 | WSW |
| 7 | SSW |
| 8 | S |
| 9 | SW |
| 10 | SE |
| 11 | NE |
| 12 | SSE |
| 13 | ENE |
| 14 | E |
| 15 | ESE |

### Wind Gust Direction Codes

| Code | Direction |
|------|-----------|
| 0 | NNW |
| 1 | NW |
| 2 | WNW |
| 3 | N |
| 4 | W |
| 5 | WSW |
| 6 | NNE |
| 7 | S |
| 8 | SSW |
| 9 | SW |
| 10 | SSE |
| 11 | NE |
| 12 | SE |
| 13 | ESE |
| 14 | ENE |
| 15 | E |

---

## Integration Guide

### Getting Started

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Test the API**
   ```bash
   curl http://localhost:5000/
   ```

3. **Get CSRF Token**
   - Navigate to `/predict` endpoint
   - Extract `csrf_token` from the form
   - Include in all POST requests

### Best Practices

1. **Always Include CSRF Token**
   - Extract from the form on page load
   - Include in every POST request

2. **Validate Input Client-Side**
   - Check ranges before submission
   - Provide user-friendly error messages

3. **Handle Errors Gracefully**
   - Check response status codes
   - Display user-friendly error messages

4. **Use Sessions**
   - Maintain session for CSRF token
   - Reuse for multiple predictions

### Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key-here
MODEL_PATH=./models/cat.pkl
FLASK_ENV=development
```

### Configuration

The API supports three environments:
- **Development:** Debug mode enabled, less strict security
- **Production:** Debug mode disabled, strict security, requires SECRET_KEY
- **Testing:** CSRF disabled, debug enabled

Set via `FLASK_ENV` environment variable:
```bash
export FLASK_ENV=production  # Linux/Mac
set FLASK_ENV=production     # Windows
```

---

## Rate Limiting

> ⚠️ **Note:** Currently, no rate limiting is implemented. Consider adding rate limiting for production deployments using Flask-Limiter.

**Recommended Implementation:**
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

---

## Future Enhancements

- [ ] RESTful JSON API endpoints
- [ ] API key authentication
- [ ] Rate limiting
- [ ] Batch prediction support
- [ ] WebSocket support for real-time predictions
- [ ] GraphQL API
- [ ] API versioning (v2)

---

## Support

For issues, questions, or contributions:
- **GitHub:** [RevSaikat/Aqua-Predict](https://github.com/RevSaikat)
- **Email:** Contact developers via LinkedIn profiles

---

**Last Updated:** November 26, 2025  
**API Version:** 1.0
