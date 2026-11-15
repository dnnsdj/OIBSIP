import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

import weather_app


def make_response(data, status_code=200):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = data
    response.raise_for_status.return_value = None
    return response


class WeatherAppTests(unittest.TestCase):
    @patch("weather_app.requests.get")
    def test_get_weather_resolves_zip_code(self, get):
        get.side_effect = [
            make_response(
                {
                    "country": "United States",
                    "places": [
                        {
                            "place name": "New York",
                            "state": "New York",
                            "latitude": "40.7128",
                            "longitude": "-74.0060",
                        }
                    ],
                }
            ),
            make_response({"current": {"temperature_2m": 20}}),
        ]

        result = weather_app.get_weather("10001-1234")

        self.assertEqual(result["location"], "New York, New York, United States")
        self.assertEqual(get.call_args_list[0].args[0], weather_app.ZIP_CODE_URL.format("10001"))
        self.assertEqual(get.call_args_list[1].kwargs["params"]["latitude"], 40.7128)

    @patch("weather_app.requests.get")
    def test_get_weather_returns_none_for_unknown_zip_code(self, get):
        get.return_value = make_response({}, status_code=404)

        self.assertIsNone(weather_app.get_weather("00000"))
        get.assert_called_once()

    def test_show_weather_displays_celsius_and_fahrenheit(self):
        output = io.StringIO()
        weather = {
            "location": "Test City",
            "current": {
                "temperature_2m": 20,
                "apparent_temperature": 21,
                "relative_humidity_2m": 50,
                "weather_code": 0,
                "wind_speed_10m": 3,
            },
        }

        with redirect_stdout(output):
            weather_app.show_weather(weather)

        self.assertIn("20 °C (68.0 °F)", output.getvalue())


if __name__ == "__main__":
    unittest.main()
