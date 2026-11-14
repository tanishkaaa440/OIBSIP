import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print("Error: the request timed out. Try again.")
        return
    except requests.exceptions.ConnectionError:
        print("Error: no internet connection.")
        return

    if response.status_code == 401:
        print("Error: invalid API key. Check your .env file.")
        return
    if response.status_code == 404:
        print("Error: city not found. Check the spelling.")
        return
    if response.status_code != 200:
        print(f"Error: something went wrong (code {response.status_code}).")
        return

    data = response.json()
    temp_c = data["main"]["temp"]
    temp_f = temp_c * 9 / 5 + 32
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind = data["wind"]["speed"]

    print(f"\nWeather in {data['name']}:")
    print(f"  Temperature: {temp_c:.1f} °C / {temp_f:.1f} °F")
    print(f"  Humidity:    {humidity}%")
    print(f"  Condition:   {description}")
    print(f"  Wind speed:  {wind} m/s\n")


def main():
    if not API_KEY:
        print("Error: API key missing. Add OWM_API_KEY to the .env file.")
        return

    while True:
        city = input("Enter city name (or 'q' to quit): ").strip()
        if city.lower() == "q":
            break
        if not city:
            print("Error: city name cannot be empty.")
            continue
        get_weather(city)


if __name__ == "__main__":
    main()
    