import requests
from bs4 import BeautifulSoup

base_url = 'http://127.0.0.1:5000'
# Get the form page to extract CSRF token
r = requests.get(f'{base_url}/predict')
if r.status_code != 200:
    print('Failed to load form page', r.status_code)
    exit()

soup = BeautifulSoup(r.text, 'html.parser')
csrf_input = soup.find('input', {'name': 'csrf_token'})
csrf_token = csrf_input['value'] if csrf_input else ''

payload = {
    'csrf_token': csrf_token,
    'date': '2024-12-20',
    'mintemp': '25',
    'maxtemp': '30',
    'rainfall': '0',
    'evaporation': '5',
    'sunshine': '8',
    'windgustspeed': '20',
    'windspeed9am': '15',
    'windspeed3pm': '25',
    'humidity9am': '60',
    'humidity3pm': '65',
    'pressure9am': '1013',
    'pressure3pm': '1015',
    'temp9am': '22',
    'temp3pm': '28',
    'cloud9am': '3',
    'cloud3pm': '4',
    'location': '10',
    'winddir9am': '1',
    'winddir3pm': '2',
    'windgustdir': '3',
    'raintoday': '0'
}

post_resp = requests.post(f'{base_url}/predict', data=payload)
print('POST status:', post_resp.status_code)
print('Response snippet:', post_resp.text[:500])
