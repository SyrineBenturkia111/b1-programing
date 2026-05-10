# Lab Exercise: EU Capitals Weather Data Collection
import requests
import json
import time

eu_capitals = [
    {"city": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"city": "Brussels", "country": "Belgium", "lat": 50.8503, "lon": 4.3517},
    {"city": "Sofia", "country": "Bulgaria", "lat": 42.6977, "lon": 23.3219},
    {"city": "Zagreb", "country": "Croatia", "lat": 45.8150, "lon": 15.9819},
    {"city": "Nicosia", "country": "Cyprus", "lat": 35.1856, "lon": 33.3823},
    {"city": "Prague", "country": "Czechia", "lat": 50.0755, "lon": 14.4378},
    {"city": "Copenhagen", "country": "Denmark", "lat": 55.6761, "lon": 12.5683},
    {"city": "Tallinn", "country": "Estonia", "lat": 59.4370, "lon": 24.7536},
    {"city": "Helsinki", "country": "Finland", "lat": 60.1695, "lon": 24.9354},
    {"city": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"city": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"city": "Athens", "country": "Greece", "lat": 37.9838, "lon": 23.7275},
    {"city": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"city": "Dublin", "country": "Ireland", "lat": 53.3498, "lon": -6.2603},
    {"city": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"city": "Riga", "country": "Latvia", "lat": 56.9496, "lon": 24.1052},
    {"city": "Vilnius", "country": "Lithuania", "lat": 54.6872, "lon": 25.2797},
    {"city": "Luxembourg", "country": "Luxembourg", "lat": 49.6116, "lon": 6.1319},
    {"city": "Valletta", "country": "Malta", "lat": 35.8989, "lon": 14.5146},
    {"city": "Amsterdam", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"city": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"city": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393},
    {"city": "Bucharest", "country": "Romania", "lat": 44.4268, "lon": 26.1025},
    {"city": "Bratislava", "country": "Slovakia", "lat": 48.1486, "lon": 17.1077},
    {"city": "Ljubljana", "country": "Slovenia", "lat": 46.0569, "lon": 14.5058},
    {"city": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"city": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686}
]

#Codes from lecture
weather_codes = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Drizzle (light)", 53: "Drizzle (moderate)", 55: "Drizzle (dense)",
    56: "Freezing Drizzle (light)", 57: "Freezing Drizzle (dense)",
    61: "Rain (slight)", 63: "Rain (moderate)", 65: "Rain (heavy)",
    66: "Freezing Rain (light)", 67: "Freezing Rain (heavy)",
    71: "Snow fall (slight)", 73: "Snow fall (moderate)", 75: "Snow fall (heavy)",
    77: "Snow grains",
    80: "Rain showers (slight)", 81: "Rain showers (moderate)", 82: "Rain showers (violent)",
    85: "Snow showers (slight)", 86: "Snow showers (heavy)",
    95: "Thunderstorm (light or moderate)", 96: "Thunderstorm with slight hail",
    97: "Thunderstorm with heavy hail"
}

API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_capital_weather(city_info):
    try:
        params = {
            "latitude": city_info["lat"],
            "longitude": city_info["lon"],
            "current_weather": True,
            "hourly": "temperature_2m,precipitation_probability,weathercode",
            "forecast_days": 1,
            "temperature_unit": "celsius",
            "windspeed_unit": "kmh"
        }
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout for {city_info['city']}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Connection error for {city_info['city']}")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for {city_info['city']}: {http_err}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {city_info['city']}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON response for {city_info['city']}")
        return None

    current = data.get("current_weather")
    if not current:
        print(f"No current_weather as a response for city: {city_info['city']}")
        return None

    weathercode = current.get("weathercode", 999)
    condition = weather_codes.get(weathercode, "Unknown")

    current_info = {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": weathercode,
        "condition": condition,
        "time": current.get("time")
    }

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precip_probs = hourly.get("precipitation_probability", [])
    codes = hourly.get("weathercode", [])

    hourly_forecast = []
    for i, t in enumerate(times):
        hourly_forecast.append({
            "time": t,
            "temperature": temps[i] if i < len(temps) else None,
            "precipitation_probability": precip_probs[i] if i < len(precip_probs) else None,
            "weathercode": codes[i] if i < len(codes) else None
        })

    result = {
        "country": city_info["country"],
        "coordinates": {
            "latitude": city_info["lat"],
            "longitude": city_info["lon"]
        },
        "current_weather": current_info,
        "hourly_forecast": hourly_forecast
    }
    return result

def main():
    all_data = {}
    total = len(eu_capitals)
    print(f"We are starting the weather collection for our {total} capitals:")

    for index, capital in enumerate(eu_capitals, 1):
        city_name = capital["city"]
        print(f"({index}/{total}) We are now fetching the weather for {city_name}:")
        result = fetch_capital_weather(capital)

        if result is not None:
            all_data[city_name] = result
            print(f" **Successfuly collected: {city_name}")
        else:
            print(f"  We are skipping city: {city_name} due to error!")

        if index < total:
            time.sleep(0.5) #0.5 seconds chosen

#Saving the collected data to a JSON file
    output_file = "eu_weather_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\nOur Weather data is saved to {output_file}")
    print(f"Finished! We collected data successfuly for {len(all_data)} out of {total} capitals!")

if __name__ == "__main__":
    main()