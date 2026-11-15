import re

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ZIP_CODE_URL = "https://api.zippopotam.us/us/{}"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Drizzle",
    53: "Drizzle",
    55: "Drizzle",
    61: "Rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Thunderstorm",
}


def get_weather(city):
    """Find a city, then get its current weather."""
    if re.fullmatch(r"\d{5}(?:-\d{4})?", city):
        location_response = requests.get(
            ZIP_CODE_URL.format(city[:5]),
            timeout=REQUEST_TIMEOUT,
        )
        if location_response.status_code == 404:
            return None

        location_response.raise_for_status()
        place_data = location_response.json()
        place = place_data["places"][0]
        latitude = float(place["latitude"])
        longitude = float(place["longitude"])
        location = ", ".join(
            part
            for part in (
                place["place name"],
                place.get("state"),
                place_data.get("country"),
            )
            if part
        )
    else:
        location_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
            timeout=REQUEST_TIMEOUT,
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results")

        if not locations:
            return None

        place = locations[0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        location = place["name"] + ", " + place.get("country", "")

    weather_response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
            "wind_speed_unit": "ms",
            "timezone": "auto",
        },
        timeout=REQUEST_TIMEOUT,
    )
    weather_response.raise_for_status()

    return {
        "location": location,
        "current": weather_response.json()["current"],
    }


def show_weather(weather):
    """Print the current weather."""
    current = weather["current"]
    code = current.get("weather_code")
    temperature_c = current.get("temperature_2m")
    temperature_f = (
        "N/A"
        if temperature_c is None
        else round(float(temperature_c) * 9 / 5 + 32, 1)
    )
    temperature_display = (
        "N/A"
        if temperature_c is None
        else f"{temperature_c} °C ({temperature_f} °F)"
    )

    print("\nWeather for", weather["location"])
    print("Conditions:", WEATHER_CODES.get(code, "Unknown"))
    print("Temperature:", temperature_display)
    print("Feels like:", current.get("apparent_temperature", "N/A"), "°C")
    print("Humidity:", current.get("relative_humidity_2m", "N/A"), "%")
    print("Wind speed:", current.get("wind_speed_10m", "N/A"), "m/s")


def main():
    city = input("Enter a city name or postal code: ").strip()
    if not city:
        print("Please enter a city name or postal code.")
        return

    try:
        weather = get_weather(city)
        if weather is None:
            print("Location not found. Check the name or postal code and try again.")
            return

        show_weather(weather)
    except requests.RequestException as error:
        print("Could not retrieve weather data:", error)
    except (ValueError, KeyError, TypeError):
        print("The weather service returned an invalid response.")


if __name__ == "__main__":
    main()
