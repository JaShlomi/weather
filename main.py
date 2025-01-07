import requests
import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timezone, timedelta


def get_coordinates(city, country=None, state=None, api_key=None):
    base_url = "http://api.openweathermap.org/geo/1.0/direct?"
    query_params = f"q={city}"

    if state:
        query_params += f",{state}"
    if country:
        query_params += f",{country}"

    query_params += f"&limit=1&appid={api_key}"
    complete_url = f"{base_url}{query_params}"

    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {'lat': round(data[0]['lat'], 3), 'lon': round(data[0]['lon'], 3)}
    return None

def get_weather_data(lat, lon, api_key=None):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    query_params = f"lat={lat}&lon={lon}&units=metric&appid={api_key}"
    complete_url = f"{base_url}{query_params}"

    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        if 'coord' in data:
            return data
    return None

def display_weather(weather_data):
    # Calculate the local time at the destination based on timezone offset
    utc_time = datetime.fromtimestamp(weather_data['dt'], timezone.utc)
    local_time = utc_time + timedelta(seconds=weather_data['timezone'])
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')

    st.image(f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png", width=60)
    st.write(f"**{weather_data['name']}**")
    st.write(f"Temp: {weather_data['main']['temp']:.2f}°C")
    st.write(f"Humidity: {weather_data['main']['humidity']}%")
    st.write(f":clock3: {formatted_time}")

# Streamlit app

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

st.title("_Weather_ :blue[Information App]   :rain_cloud::sun_small_cloud:")

# Create a single container for the entire app
main_container = st.container()

# 3 columns: Search, Weather Data & Map, Major Cities
with main_container:
    col1, col2, col3 = st.columns([1.8, 2.4, 6.2])

    with col1:
        st.header(":red[Location:]")
        city_name = st.text_input("Enter city name", key="city")
        country_code = st.text_input("Enter country code (optional)", key="country")
        state_name = st.text_input("Enter state (optional)", key="state")

        if st.button("Get Weather"):
            coordinates = get_coordinates(city_name, country_code, state_name, api_key=st.secrets['secret_key'])
            if coordinates:
                st.session_state.coordinates = coordinates
            else:
                st.error("Failed to fetch coordinates. Please check your input or try again later.")

    with col2:
        st.header(":red[Weather at:]")
        if 'coordinates' in st.session_state and st.session_state.coordinates:
            weather_data = get_weather_data(st.session_state.coordinates['lat'], st.session_state.coordinates['lon'], api_key=st.secrets['secret_key'])
            if weather_data:
                display_weather(weather_data)
                df = pd.DataFrame({'lat': [st.session_state.coordinates['lat']], 'lon': [st.session_state.coordinates['lon']]})
                st.map(df, use_container_width=True, height=200)
            else:
                st.error("Failed to fetch weather data. Please try again later.")

    with col3:
        st.header(":red[Major Cities Weather:]")
        city_coordinates = [
            ("Tel Aviv", 32.083, 34.783),
            ("Jerusalem", 31.768, 35.214),
            ("Haifa", 32.794, 34.989),
            ("Eilat", 29.558, 34.951),
            ("Paris", 48.857, 2.352),
            ("London", 51.507, -0.128),
            ("New York", 40.713, -74.006),
            ("Los Angeles", 34.052, -118.244),
            ("Miami", 25.761, -80.191),
            ("Dallas", 32.776, -96.797),
            ("Boston", 42.360, -71.058),
            ("Toronto", 43.653, -79.383),
            ("Rio de Janeiro", -22.907, -43.173),
            ("Sydney", -33.869, 151.209),
            ("Tokyo", 35.690, 139.692),
            ("Moscow", 55.756, 37.617),
            ("Beijing", 39.904, 116.407),
            ("Mumbai", 19.076, 72.878),
            ("Cairo", 30.044, 31.236),
            ("Cape Town", -33.926, 18.423),
            ("Berlin", 52.520, 13.405),
            ("Madrid", 40.417, -3.704),
            ("Rome", 41.903, 12.496),
            ("Chicago", 41.878, -87.630),
            ("Dubai", 25.205, 55.271),
            ("Hong Kong", 22.286, 114.158),
            ("Bangkok", 13.754, 100.502),
            ("Singapore", 1.290, 103.850),
            ("Istanbul", 41.008, 28.978),
            ("Seoul", 37.567, 126.978),
            ("Mexico City", 19.433, -99.133),
            ("Buenos Aires", -34.604, -58.382),
            ("Jakarta", -6.209, 106.846),
            ("Lagos", 6.455, 3.394),
            ("Lima", -12.046, -77.043),
            ("Sao Paulo", -23.551, -46.633),
            ("Karachi", 25.120, 67.001),
            ("Kinshasa", -4.337, 15.327),
            ("Bogota", 4.610, -74.072),
            ("Vancouver", 49.2827, -123.1207),
            ("San Francisco", 37.7749, -122.4194),
            ("Shanghai", 31.2304, 121.4737),
            ("Nairobi", -1.286389, 36.817223),
            ("Johannesburg", -26.2041, 28.0473),
            ("Accra", 5.6037, -0.1870),
            ("Addis Ababa", 9.0301, 38.7200),
            ("Casablanca", 33.5731, -7.5898),
            ("Tunis", 36.8065, 10.1815)
        ]

        # Create an area to refresh the weather data
        refresh_area = st.empty()

        while True:
            with refresh_area:
                cols = st.columns(5)
                tel_aviv_data = get_weather_data(32.083, 34.783, api_key=st.secrets['secret_key'])
                if tel_aviv_data:
                    with cols[0]:
                        display_weather(tel_aviv_data)
                else:
                    st.error("Failed to fetch weather data for Tel Aviv. Please try again later.")

                selected_cities = random.sample(city_coordinates[1:], k=4)
                for i, (city_name, lat, lon) in enumerate(selected_cities):
                    weather_data = get_weather_data(lat, lon, api_key=st.secrets['secret_key'])
                    if weather_data:
                        with cols[i + 1]:
                            display_weather(weather_data)
                    else:
                        st.error(f"Failed to fetch weather data for {city_name}. Please try again later.")

            time.sleep(2)

