from typing import Dict
from bot.weather import *
from langchain.tools import tool


@tool
def calculate(exper: str) -> float:
    """
    Perform the simple mathematical operation. Like multiply add divide subtract or combination of these.
    Expected expression 'x*y-z', x+y, c-b

    Args:
        expression (str): A mathematical expression.

    Returns:
        float: Result of the evaluated expression.
    """
    if type(exper) == "str":
        out = eval(exper)

    else:
        out = eval(str(exper))

    res = f"The output of expression {exper} is {out} "
    return res


@tool
def small_talks(query: str) -> Dict:
    """
    When aked general query and random text.

    Args:
        query: Str

    Returns:
        JSON object or python dictonary.
    """
    return None


@tool
def get_weather_for_city(city_name: str) -> dict:
    """
    Get current weather by city name.

    Args:
        city_name (str): Name of the city.

    Returns:
        dict: Weather data or error message.
    """

    lat, lon = get_coordinates_from_city(city_name)
    if lat is None or lon is None:
        return {
            "error": f"Could not find data for city '{city_name}'. Please provide a valid city name."
        }

    return get_current_weather(lat, lon)
