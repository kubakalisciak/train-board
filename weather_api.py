import requests
import time


def get_response(url):
    return requests.get(url).json()


def get_weather_data(response):
    hour = time.strftime("%H")
    temperature = response['hourly']['temperature_2m'][int(hour)]
    humidity = response['hourly']['relative_humidity_2m'][int(hour)]
    precipitacion = response['hourly']['precipitation'][int(hour)]
    wind_speed = response['hourly']['wind_speed_10m'][int(hour)]
    wind_direction = response['hourly']['wind_direction_10m'][int(hour)]
    return {
        'temperature': temperature,
        'humidity': humidity,
        'precipitation': precipitacion,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction}


def main():
    data = get_weather_data(get_response('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m&forecast_days=1'))
    
    print(f"Today is {time.strftime('%A, %d.%m.%Y')}")
    print(f"It is {data['temperature']} degrees, {data['humidity']}% humidity, {data['precipitation']} mm of precipitation and {data['wind_speed']} m/s wind speed going from {data['wind_direction']} degrees")


if __name__ == "__main__":
    main()
