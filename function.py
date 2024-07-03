# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:13:56 2024

@author: Chancy
"""
import requests
import pandas as pd

# Weather API URL and headers
url = 'https://weatherunion.com/gw/weather/external/v0/get_weather_data'
headers = {
    'x-zomato-api-key': 'b16e52aa254f8eb99ddc98b642146ae4'
}

api_key = '5b3ce3597851110001cf624852bc21a822034504a103585fcd59c3f2'

# Function to call the weather API for each locality and save the response in the DataFrame
def get_weather_data_for_localities(df):
    url = 'https://weatherunion.com/gw/weather/external/v0/get_locality_weather_data'
    headers = {
        'x-zomato-api-key': 'b16e52aa254f8eb99ddc98b642146ae4'
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

def color_heat_index(val):
    return f'background-color: {get_marker_color(val)}'

# Function to read the Excel file
def read_excel(file):
    return pd.read_excel(file)

# Function to filter data based on city and device type
def filter_city_data(df, city_name):
    return df[(df['cityName'] == city_name) & (df['device_type'] == "1 - Automated weather system")]

# Function to fetch OSM data
def fetch_osm_data(bbox, tags):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
        {"".join([f'node["{tag.split("=")[0]}"="{tag.split("=")[1]}"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});' for tag in tags])}
    );
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

# Function to calculate bounding box based on city coordinates
def get_bounding_box(center, radius=0.1):
    lat, lon = center
    return [lat-radius, lon-radius, lat+radius, lon+radius]

# Define the function to generate conditions
def generate_conditions(merged_df):
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
    return conditions

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
        temp = int(round(float(temp)))
        humidity = int(round(float(humidity)))
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
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 31:
            return "Caution"
        elif 32 <= temp <= 35:
            return "Extreme Caution"
        elif 36 <= temp <= 40:
            return "Danger"
        elif 41 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 50:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 30:
            return "Caution"
        elif 31 <= temp <= 34:
            return "Extreme Caution"
        elif 35 <= temp <= 39:
            return "Danger"
        elif 40 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 55:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 30:
            return "Caution"
        elif 31 <= temp <= 33:
            return "Extreme Caution"
        elif 34 <= temp <= 38:
            return "Danger"
        elif 39 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 60:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 29:
            return "Caution"
        elif 30 <= temp <= 32:
            return "Extreme Caution"
        elif 33 <= temp <= 37:
            return "Danger"
        elif 38 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 65:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 29:
            return "Caution"
        elif 30 <= temp <= 32:
            return "Extreme Caution"
        elif 33 <= temp <= 36:
            return "Danger"
        elif 37 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 70:
        if temp < 26:
            return "Safe"
        elif 27 <= temp <= 28:
            return "Caution"
        elif 29 <= temp <= 31:
            return "Extreme Caution"
        elif 32 <= temp <= 35:
            return "Danger"
        elif 36 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 75:
        if temp < 26:
            return "Safe"
        elif 27 < temp <= 28:
            return "Caution"
        elif 29 <= temp <= 31:
            return "Extreme Caution"
        elif 32 <= temp <= 35:
            return "Danger"
        elif 36 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 80:
        if temp < 26:
            return "Safe"
        elif temp <= 27:
            return "Caution"
        elif temp <= 28:
            return "Extreme Caution"
        elif 29 <= temp <= 30:
            return "Danger"
        elif 31 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 85:
        if temp < 26:
            return "Safe"
        elif temp <= 27:
            return "Caution"
        elif 28 <= temp <= 30:
            return "Extreme Caution"
        elif 31 <= temp <= 33:
            return "Danger"
        elif 34 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 90:
        if temp < 26:
            return "Safe"
        elif temp <= 27:
            return "Caution"
        elif 28 <= temp <= 29:
            return "Extreme Caution"
        elif 30 <= temp <= 33:
            return "Danger"
        elif 34 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 95:
        if temp < 26:
            return "Safe"
        elif temp <= 27:
            return "Caution"
        elif 28 <= temp <= 29:
            return "Extreme Caution"
        elif 30 <= temp <= 31:
            return "Danger"
        elif 32 <= temp <= 43:
            return "Extreme Danger"
    elif humidity <= 100:
        if temp < 26:
            return "Safe"
        elif temp <= 27:
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
    
# Function to get route from OpenRouteService API
def get_route(start_coords, end_coords, api_key):
    route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_coords[1]},{start_coords[0]}&end={end_coords[1]},{end_coords[0]}"
    response = requests.get(route_url).json()
    
    if 'features' in response:
        route_coords = response['features'][0]['geometry']['coordinates']
        # Convert coordinates from (longitude, latitude) to (latitude, longitude)
        route = [(coord[1], coord[0]) for coord in route_coords]
        return route
    
    return None

# Function to check if route passes through high-temperature locations within a buffer
def route_passes_high_temp(route, high_temp_locations, buffer_radius_km=2):
    buffer_radius_deg = buffer_radius_km / 111.32  # Approximate degrees per kilometer
    
    for point in route:
        for _, location in high_temp_locations.iterrows():
            distance = ((point[0] - location['latitude'])**2 + (point[1] - location['longitude'])**2)**0.5
            if distance < buffer_radius_deg:
                return True
    return False


def geocode_location(location):
    
    url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={location}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad response status

        if response.status_code == 200:
            data = response.json()
            if data and 'features' in data and len(data['features']) > 0:
                # Extract coordinates from the first result
                coordinates = data['features'][0]['geometry']['coordinates']
                return coordinates[1], coordinates[0]  # Latitude, Longitude
            else:
                print(f"No coordinates found for location: {location}")
        else:
            print(f"Error fetching coordinates for {location}: Status Code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    return None

# Function to get location suggestions from OpenRouteService API
def get_location_suggestions(query):
    url = f"https://api.openrouteservice.org/geocode/autocomplete?api_key={api_key}&text={query}"
    response = requests.get(url).json()
    suggestions = [feature['properties']['label'] for feature in response['features']]
    print(suggestions)
    return suggestions
 