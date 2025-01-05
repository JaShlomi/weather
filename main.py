import streamlit as st
import requests

def get_weather_data(city, country=None, state=None, api_key='2962c0531021bfa04c3a252c316c4437'):
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

# Streamlit app
def web_temp():
  st.title("Weather App")

  city_name = st.text_input("Enter City Name:")
  country_code = st.text_input("Enter Two-Letter Country Code (optional):")
  city_state = st.text_input("Enter State/Region (optional):")

  if st.button("Get Weather"):
    if country_code and city_state:
      weather_info = get_weather_data(city_name, country_code, city_state)
    elif country_code:
      weather_info = get_weather_data(city_name, country_code)
    elif city_state:
      weather_info = get_weather_data(city_name, state=city_state)
    else:
      weather_info = get_weather_data(city_name)

    if weather_info:
      st.success(f"Weather in {city_name}:")
      st.write(f"Temperature: {weather_info['temperature']:.2f}°C")
      st.write(f"Weather Condition: {weather_info['description']}")
      st.write(f"Humidity: {weather_info['humidity']}%")

if __name__ == "__main__":
  web_temp()
