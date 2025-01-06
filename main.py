'''import streamlit as st
import requests

def get_weather_data(city, country=None, state=None, api_key=None):
  """
  Fetches weather data for a given city using the OpenWeatherMap API.

  Args:
    city: The name of the city.
    country: The two-letter country code (optional).
    state: The state or region (optional).
    api_key: Your OpenWeatherMap API key.

  Returns:
    A dictionary containing temperature, weather description, and humidity,
    or None if the city is not found or an error occurs.
  """

  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  query_params = f"appid={api_key}&units=metric"

  if country and state:
    query_params += f"&q={city},{state},{country}"
  elif country:
    query_params += f"&q={city},{country}"
  elif state:
    query_params += f"&q={city},{state}"
  else:
    query_params += f"&q={city}"

  complete_url = f"{base_url}{query_params}"

  try:
    response = requests.get(complete_url)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    for key, value in data.items():
      print(f"{key}: {value}")


    if data['cod'] == 200:
      weather_data = {
          'temperature': data['main']['temp'],
          'description': data['weather'][0]['description'],
          'humidity': data['main']['humidity']
      }
      return weather_data
    else:
      st.error(f"City '{city}' not found.")
      return None

  except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
    return None

result = get_weather_data(city = 'london',api_key='2962c0531021bfa04c3a252c316c4437')

# Streamlit app
def web_temp():
  st.title("Weather App")

  city_name = st.text_input("Enter City Name:")
  country_code = st.text_input("Enter Two-Letter Country Code (optional):")
  city_state = st.text_input("Enter State/Region (optional):")

  if st.button("Get Weather"):
    if country_code and city_state:
      weather_info = get_weather_data(city_name, country_code, city_state,api_key = st.secrets['secret_key'])
    elif country_code:
      weather_info = get_weather_data(city_name, country_code, api_key = st.secrets['secret_key'])
    elif city_state:
      weather_info = get_weather_data(city_name, city_state, api_key = st.secrets['secret_key'])
    else:
      weather_info = get_weather_data(city_name, api_key = st.secrets['secret_key'])

    if weather_info:
      st.success(f"Weather in {city_name}:")
      st.write(f"Temperature: {weather_info['temperature']:.2f}°C")
      st.write(f"Weather Condition: {weather_info['description']}")
      st.write(f"Humidity: {weather_info['humidity']}%")

if __name__ == "__main__":
  web_temp()'''
import requests
from datetime import datetime
import streamlit as st

def get_coordinates(city, country=None, api_key=None):
    base_url = "http://api.openweathermap.org/geo/1.0/direct?"
    query_params = f"q={city}"

    if country:
        query_params += f",{country}"

    query_params += f"&limit=1&appid={api_key}"
    complete_url = f"{base_url}{query_params}"

    response = requests.get(complete_url)
    data = response.json()

    if data:
        return {
            'lat': round(data[0]['lat'], 2),
            'lon': round(data[0]['lon'], 2)
        }
    else:
        return None

def get_weather_data(lat, lon, api_key=None):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    query_params = f"lat={lat}&lon={lon}&units=metric&appid={api_key}"
    complete_url = f"{base_url}{query_params}"

    response = requests.get(complete_url)
    data = response.json()

    if 'coord' in data:
        return data
    else:
        return None

def display_weather(weather_data):
    st.write(f"Weather in {weather_data['name']}:")
    st.write(f"Temperature: {weather_data['main']['temp']:.2f}°C")
    st.write(f"Weather Condition: {weather_data['weather'][0]['description']}")
    st.write(f"Humidity: {weather_data['main']['humidity']}%")
    st.write(f"{weather_data['name']} Time: {datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Local Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.image(f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png", caption="Weather Icon")

# Streamlit app
st.title("Weather Information")

# Major cities section
st.header("Major Cities")
cities = ["Paris", "London", "New York", "Los Angeles", "Rio de Janeiro", "Sydney", "Tokyo", "Moscow", "Beijing", "Mumbai", "Cairo", "Cape Town"]
country_codes = ["FR", "GB", "US", "US", "BR", "AU", "JP", "RU", "CN", "IN", "EG", "ZA"]

for city, country in zip(cities, country_codes):
    coordinates = get_coordinates(city, country, api_key=st.secrets['secret_key'])
    if coordinates:
        weather_data = get_weather_data(coordinates['lat'], coordinates['lon'], api_key=st.secrets['secret_key'])
        if weather_data:
            display_weather(weather_data)
            st.write("---")

# Specific destination section
st.header("Specific Destination")
city_name = st.text_input("Enter city name")
country_code = st.text_input("Enter country code (optional)")

if st.button("Get Weather"):
    coordinates = get_coordinates(city_name, country_code, api_key=st.secrets['secret_key'])
    if coordinates:
        weather_data = get_weather_data(coordinates['lat'], coordinates['lon'], api_key=st.secrets['secret_key'])
        if weather_data:
            display_weather(weather_data)
        else:
            st.error("Weather data not found. Please try again.")
    else:
        st.error("City not found or an error occurred. Please try again.")