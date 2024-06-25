import streamlit as st
import folium
import requests
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

# Function to read the Excel file
def read_excel(file):
    return pd.read_excel(file)

# Function to filter data based on city and device type
def filter_city_data(df, city_name):
    return df[(df['cityName'] == city_name) & (df['device_type'] == "1 - Automated weather system")]

# Example usage
uploaded_file = 'C:/Users/Chancy/Desktop/Weather_Station_Id.xlsx'  # Replace with the path to your file

df = read_excel(uploaded_file)


# List of cities for the dropdown
cities = ['Select City', 'Delhi NCR', 'Kolkata', 'Mumbai', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai']

st.title('Geo-Heat Shield: A Geospatial Approach to Heatwave Resilience')

# Dropdown to select city
selected_city = st.sidebar.selectbox('Select a city', cities)

# Dictionary of city coordinates
city_coordinates = {
    'Delhi NCR': (28.630630, 77.220640),
    'Kolkata': (22.5744, 88.3629),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (13.040495, 77.569420), 
    'Pune': (18.5204, 73.8567),
    'Hyderabad': (17.4065, 78.4772),
    'Chennai': (13.0843, 80.2705)
}

# Weather API URL and headers
url = 'https://weatherunion.com/gw/weather/external/v0/get_weather_data'
headers = {
    'x-zomato-api-key': '6e3fc4ad038dfe1c329e91503d86d672'
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

def determine_heat_index(temp, humidity):
    if temp is None or humidity is None:
        return "N/A"

    # Ensure temperature and humidity are converted to float
    try:
        temp = float(temp)
        humidity = float(humidity)
    except ValueError:
        return "N/A"

    #print(f"Temp: {temp}, Humidity: {humidity}")  # Debug line

    if humidity < 40:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 32:
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
        elif 39 <= temp <= 43:
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
        elif 37 <= temp <= 43:
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
        elif temp == 30:
            return "Danger"
        elif 31 <= temp <= 43:
            return "Extreme Danger"
    
    return "N/A"  # Default case if no condition is met


# Function to get marker color based on heat index category
def get_marker_color(heat_index):
    if heat_index == "Safe":
        return "lightgreen"
    elif heat_index == "Caution":
        return "green"
    elif heat_index == "Extreme Caution":
        return "orange"
    elif heat_index == "Danger":
        return "red"
    elif heat_index == "Extreme Danger":
        return "darkred"
    else:
        return "blue"  # Default color for "N/A"
    
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
        heat_index = "N/A"
    
    marker_color = get_marker_color(heat_index)
    
    folium.Marker(
        location=coords,
        popup=popup_content,
        tooltip=f"{city}",
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

# Function to call the weather API for each locality and save the response in the DataFrame
def get_weather_data_for_localities(df):
    url = 'https://weatherunion.com/gw/weather/external/v0/get_locality_weather_data'
    headers = {
        'x-zomato-api-key': '6e3fc4ad038dfe1c329e91503d86d672'
    }
    
    weather_data_list = []
    for index, row in df.iterrows():
        params = {
            'locality_id': row['localityId']
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            weather_data = response.json()
            weather_data['localityId'] = row['localityId']
            weather_data_list.append(weather_data)
        else:
            print(f"Failed to retrieve data for {row['localityName']}: {response.status_code}")
    
    # Create a DataFrame from weather_data_list
    weather_df = pd.DataFrame(weather_data_list)
    
    # Extract specific fields from locality_weather_data dictionary
    weather_df['temperature'] = weather_df['locality_weather_data'].apply(lambda x: x.get('temperature', None))
    weather_df['humidity'] = weather_df['locality_weather_data'].apply(lambda x: x.get('humidity', None))
    weather_df['wind_speed'] = weather_df['locality_weather_data'].apply(lambda x: x.get('wind_speed', None))
        
    # Drop the original 'locality_weather_data' column
    weather_df.drop(columns=['locality_weather_data'], inplace=True)
    
    # Drop rows where temperature or humidity is NaN
    weather_df.dropna(subset=['temperature', 'humidity'], inplace=True)
    return weather_df


# If a specific city is selected, zoom to that city
if selected_city != 'Select City':
    m.location = city_coordinates[selected_city]
    m.zoom_start = 10

    # Filter the data based on the selected city
    filtered_df = filter_city_data(df, selected_city)
    #print(filtered_df)

    weather_df = get_weather_data_for_localities(filtered_df)
    # Merge the weather data with the original filtered DataFrame
    merged_df = pd.merge(filtered_df, weather_df, on='localityId')
   
    conditions = [
    (merged_df['temperature'] < 27) & (merged_df['humidity'] < 40),   
    
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 27) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 28) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 29) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 30) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 31) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 32) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 33) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 34) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 35) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 36) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 37) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 38) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 39) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 40) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 41) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 42) & (merged_df['humidity'] <= 100),
    
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 40),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 45),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 50),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 55),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 60),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 65),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 70),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 75),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 80),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 85),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 90),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 95),
    (merged_df['temperature'] <= 43) & (merged_df['humidity'] <= 100),

    ]
    
    choices = [merged_df['temperature'], 
               27,27,27,28,28,28,29,29,30,30,31,31,32,
               28,28,28,29,29,30,31,31,32,33,34,35,36,
               29,29,30,30,31,32,33,34,35,36,37,38,40,
               30,30,31,32,33,34,35,36,38,39,41,42,44,
               31,32,33,34,35,36,38,39,41,43,45,47,49,
               32,33,35,36,37,39,40,42,44,47,49,51,56,
               34,35,36,38,40,41,43,46,48,51,54,57,57,
               35,37,38,40,42,44,47,49,52,55,55,55,55,
               37,39,41,43,45,48,50,53,57,57,57,57,57,
               39,41,43,46,48,51,54,58,58,58,58,58,58,
               41,43,46,48,51,55,58,58,58,58,58,58,58,
               43,46,49,52,55,59,59,59,59,59,59,59,59,
               46,49,52,54,59,59,59,59,59,59,59,59,59,
               48,51,55,58,58,58,58,58,58,58,58,58,58,
               51,54,58,58,58,58,58,58,58,58,58,58,58,
               54,57,57,57,57,57,57,57,57,57,57,57,57,
               57,57,57,57,57,57,57,57,57,57,57,57,57]
    
    merged_df['feels_like'] = np.select(conditions, choices, default=None)

    print(merged_df)
    heat_data = [[row['latitude'], row['longitude'], row['feels_like']] for index, row in merged_df.iterrows()]
    HeatMap(heat_data).add_to(m)
    
# Render the map using components.html
map_html = m._repr_html_()
components.html(map_html, height=500)
