import streamlit as st
import folium
import requests
import streamlit.components.v1 as components

# List of cities for the dropdown
cities = ['Select City', 'New Delhi', 'Kolkata', 'Mumbai', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai']

st.title('Geo-Heat Shield: A Geospatial Approach to Heatwave Resilience')

# Dropdown to select city
selected_city = st.sidebar.selectbox('Select a city', cities)

# Dictionary of city coordinates
city_coordinates = {
    'New Delhi': (28.6139, 77.2088),
    'Kolkata': (22.5744, 88.3629),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946), 
    'Pune': (18.5204, 73.8567),
    'Hyderabad': (17.4065, 78.4772),
    'Chennai': (13.0843, 80.2705)
}

# Weather API URL and headers
url = 'https://weatherunion.com/gw/weather/external/v0/get_weather_data'
headers = {
    'x-zomato-api-key': '70c5ad038be8ab5f0ca32ab0da764120'
}

# Function to fetch weather data for a given location
def get_weather_data(latitude, longitude):
    params = {
        'latitude': latitude,
        'longitude': longitude
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to determine heat index category based on temperature and humidity
def determine_heat_index(temp, humidity):
    if humidity is None or temp is None:
        return "N/A"
    
    if temp <= 26:
            return "Safe"
    elif humidity < 40:
        if 27 <= temp <= 32:
            return "Caution"
        elif 33 <= temp <= 36:
            return "Extreme Caution"
        elif 37 <= temp <= 41:
            return "Danger"
        elif 42 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 45:
        if 27 <= temp <= 31:
            return "Caution"
        elif 32 <= temp <= 35:
            return "Extreme Caution"
        elif 36 <= temp <= 40:
            return "Danger"
        elif 41 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 50:
        if 27 <= temp <= 30:
            return "Caution"
        elif 31 <= temp <= 34:
            return "Extreme Caution"
        elif 35 <= temp <= 39:
            return "Danger"
        elif 40 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 55:
        if 27 <= temp <= 30:
            return "Caution"
        elif 31 <= temp <= 33:
            return "Extreme Caution"
        elif 34 <= temp <= 38:
            return "Danger"
        elif 38 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 60:
        if 27 <= temp <= 29:
            return "Caution"
        elif 30 <= temp <= 32:
            return "Extreme Caution"
        elif 33 <= temp <= 37:
            return "Danger"
        elif 38 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 65:
        if 27 <= temp <= 29:
            return "Caution"
        elif 30 <= temp <= 32:
            return "Extreme Caution"
        elif 33 <= temp <= 36:
            return "Danger"
        elif 38 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 70:
        if 27 <= temp <= 28:
            return "Caution"
        elif 29 <= temp <= 31:
            return "Extreme Caution"
        elif 32 <= temp <= 35:
            return "Danger"
        elif 36 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 75:
        if 27 <= temp <= 28:
            return "Caution"
        elif 29 <= temp <= 31:
            return "Extreme Caution"
        elif 32 <= temp <= 35:
            return "Danger"
        elif 36 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 80:
        if temp <= 27:
            return "Caution"
        elif temp <= 28:
            return "Extreme Caution"
        elif 29 <= temp <= 30:
            return "Danger"
        elif 31 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 85:
        if temp <= 27:
            return "Caution"
        elif 28 <= temp <= 30:
            return "Extreme Caution"
        elif 31 <= temp <= 33:
            return "Danger"
        elif 34 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 90:
        if temp <= 27:
            return "Caution"
        elif 28 <= temp <= 29:
            return "Extreme Caution"
        elif 30 <= temp <= 33:
            return "Danger"
        elif 34 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 95:
        if temp <= 27:
            return "Caution"
        elif 28 <= temp <= 29:
            return "Extreme Caution"
        elif 30 <= temp <= 31:
            return "Danger"
        elif 32 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 100:
        if temp <= 27:
            return "Caution"
        elif 28 <= temp <= 29:
            return "Extreme Caution"
        elif temp <= 30:
            return "Danger"
        elif 32 <= temp <= 43:
            return "Extreme Danger"
    # Continue this pattern for other humidity ranges as needed
    return "N/A"

# Create a folium Map instance centered on India
initial_center = (20.5937, 78.9629)
zoom_level = 5 if selected_city == 'Select City' else 10
m = folium.Map(location=initial_center, zoom_start=zoom_level)

# Fetch weather data and add markers for all cities
for city, coords in city_coordinates.items():
    weather_data = get_weather_data(coords[0], coords[1])
    if weather_data and weather_data['message'] != 'temporarily unavailable':
        weather = weather_data.get('locality_weather_data', {})
        temp = weather.get('temperature', 'N/A')
        humidity = weather.get('humidity', 'N/A')
        heat_index = determine_heat_index(temp, humidity) if temp != 'N/A' and humidity != 'N/A' else "N/A"
        popup_content = f"<h3>Weather in {city}</h3>"
        popup_content += f"<p>Temperature: {temp} °C</p>"
        popup_content += f"<p>Humidity: {humidity}%</p>"
        popup_content += f"<p>Heat Index: {heat_index}</p>"
    else:
        popup_content = f"<h3>Weather data not available for {city}</h3>"
    
    folium.Marker(
        location=coords,
        popup=popup_content,
        tooltip=f"{city}",
    ).add_to(m)

# If a specific city is selected, zoom to that city
if selected_city != 'Select City':
    m.location = city_coordinates[selected_city]
    m.zoom_start = 10

# Render the map using components.html
map_html = m._repr_html_()
components.html(map_html, height=500)
