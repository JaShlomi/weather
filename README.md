# Weather App with a Tweak

This Python-based weather app fetches and displays weather data for a specified city and country. It also shows weather data for five major cities, refreshing every 8 seconds, with Tel Aviv always included.

**[Demo on Streamlit](https://weather-xcyw6hnvu2izthjrv2tqm2.streamlit.app/)**

## Features
- Input city and country to get weather data.
- Fetches latitude and longitude using the OpenWeather Geocoding API.
- Displays weather data using Streamlit.
- Shows weather data for five major cities, refreshing every 8 seconds.
- Tel Aviv is always displayed, with four other cities being refreshed.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/JaShlomi/weather
    ```
2. Navigate to the project directory:
    ```bash
    cd weather-app
    ```
3. Install the required packages using Poetry:
    ```bash
    poetry install
    ```

## Usage
1. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```
2. Enter the city and country code (optional), state (optional) to get the weather data.

## Dependencies
- Python 3.12
- Streamlit 1.41.1
- Requests 2.32.3
- Pandas 2.2.3
- Seaborn 0.13.2
- Plotly 5.24.1
- Jason 0.1.7
- Datetime 5.5

## OpenWeather API
Sign up at OpenWeather to get an API key.

### Current Weather Data API
Endpoint: `https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}`

### Geocoding API
Endpoint: `http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={API key}`

## Main Functions

### `get_coordinates`
**Purpose:** Fetches the latitude and longitude of a city using the OpenWeather Geocoding API.

**Parameters:**
- `city`: The name of the city.
- `country` (optional): The country code.
- `state` (optional): The state code.
- `api_key`: Your OpenWeather API key.

**Returns:** A dictionary with latitude and longitude if successful, otherwise `None`.

**Explanation:** This function constructs a URL with the provided city, state, and country parameters, and sends a request to the OpenWeather Geocoding API. If the request is successful and data is returned, it extracts and rounds the latitude and longitude values.

### `get_weather_data`
**Purpose:** Fetches weather data for a given latitude and longitude using the OpenWeather Weather API.

**Parameters:**
- `lat`: Latitude of the location.
- `lon`: Longitude of the location.
- `api_key`: Your OpenWeather API key.

**Returns:** Weather data in JSON format if successful, otherwise `None`.

**Explanation:** This function constructs a URL with the provided latitude and longitude, and sends a request to the OpenWeather Weather API. If the request is successful and data is returned, it extracts the weather data.

### `display_weather`
**Purpose:** Displays weather information using Streamlit.

**Parameters:**
- `weather_data`: The weather data to display.

**Displays:** Weather icon, city name, temperature, humidity, description, and local time.

**Explanation:** This function formats and displays the weather data using Streamlit. It calculates the local time based on the timezone offset, formats the time, and displays the weather icon, city name, temperature, humidity, description, and local time.

## Refresh Interval
The app refreshes every 8 seconds to comply with the OpenWeather API's limit of 60 calls per minute.

## Course Information
This project is an open-source initiative developed as part of the BIU IL DS18 course.

## Running the App on the Web
You can also run the Streamlit app directly on the web based on the main.py file in the GitHub repository. This allows you to access the app without needing to install any dependencies locally.

## Running the App - loacl
To run the app, use the following command:
```bash
streamlit run main.p

