import requests


def get_coordinates_from_city(city: str) -> tuple:
    """
    Convert a city name to (latitude, longitude) using Open-Meteo's geocoding API.

    Args:
        city (str): Name of the city to geocode.

    Returns:
        tuple[float, float]: (latitude, longitude) of the city.
            Returns (None, None) if city not found or on error.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return None, None

        location = data["results"][0]
        return location["latitude"], location["longitude"]

    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None, None


def get_current_weather(lat: float, lon: float) -> dict:
    """
    Get current weather using the Open-Meteo API.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict: Weather data including temperature, windspeed, and time.
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = data.get("current_weather", {})
        return {
            "temperature (°C)": weather.get("temperature"),
            "windspeed (km/h)": weather.get("windspeed"),
            "weather_code": weather.get("weathercode"),
            "time": weather.get("time"),
        }
    except Exception as e:
        return {"error": str(e)}


# # 🔍 Example usage:
# if __name__ == "__main__":
#     city = input("Enter city name: ")
#     weather = get_weather_for_city(city)
#     print(weather)
