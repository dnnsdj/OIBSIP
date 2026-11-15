# Command-line Weather App

Fetches current weather from Open-Meteo for a city or postal code.

## Setup

1. Install the dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Run the application:

   ```powershell
   python weather_app.py
   ```

Enter a city name or US ZIP code when prompted. The app displays the current
temperature in Celsius and Fahrenheit, humidity, conditions, and wind speed.
Open-Meteo provides weather data, and Zippopotam.us resolves US ZIP codes. No
API key is required.
