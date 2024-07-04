import streamlit as st
import folium
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
import branca.colormap as cm
import plotly.express as px
from streamlit_searchbox import st_searchbox
from function import read_excel, filter_city_data ,fetch_osm_data , get_bounding_box
from function import generate_conditions, get_weather_data, determine_heat_index , get_marker_color , get_weather_data_for_localities ,color_heat_index
from function import get_location_suggestions, geocode_location, route_passes_high_temp, get_route

st.set_page_config(layout="wide")
 
uploaded_file = 'Weather_Station_Id.xlsx'  # Replace with the path to your file

df = read_excel(uploaded_file)

# List of cities for the dropdown
cities = ['Select City', 'Delhi NCR', 'Kolkata', 'Mumbai', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai']

st.title('Geo-Heat Shield: A Geospatial Approach to Heatwave Resilience')

selected_city = st.sidebar.selectbox('Select a city', cities)

# Dictionary of city coordinates
city_coordinates = {
    'Delhi NCR': (28.676018, 77.208446),
    'Kolkata': (22.5744, 88.3629),
    'Mumbai': (19.108639,72.874437),
    'Bengaluru': (13.040495, 77.569420), 
    'Pune': (18.5204, 73.8567),
    'Hyderabad': (17.392120, 78.494443),
    'Chennai': (13.0843, 80.2705)
}

# Create a folium Map instance centered on India
initial_center = (20.5937, 78.9629)
zoom_level = 4 if selected_city == 'Select City' else 10
m = folium.Map(location=initial_center, zoom_start=zoom_level,tiles="cartodbpositron")

weather_data_list = []

# Fetch weather data and add markers for all cities
for city, coords in city_coordinates.items():
    weather_data = get_weather_data(coords[0], coords[1])
    if weather_data and weather_data['message'] != 'temporarily unavailable':
        weather = weather_data.get('locality_weather_data', {})
        #print(weather)
        temp = weather.get('temperature', 'N/A')
        humidity = weather.get('humidity', 'N/A')
        heat_index = determine_heat_index(temp, humidity) if temp != 'N/A' and humidity != 'N/A' else "N/A"
        
        # Store weather data in a dictionary
        city_weather = {
            'City': city,
            'temperature': temp,
            'humidity': humidity,
            'Heat Index': heat_index
        }
        # Append dictionary to the list
        weather_data_list.append(city_weather)
       
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
    
# Define HTML for the legend
legend_html = '''
<div style="
    position: fixed;
    bottom: 100px;
    left: 10px;
    width: 100px;
    height: 100px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:10px;
    ">
    &nbsp;<b>Heat Index Legend</b><br>
    &nbsp;<i class="fa fa-circle" style="color:lightgreen"></i>&nbsp;Safe<br>
    &nbsp;<i class="fa fa-circle" style="color:green"></i>&nbsp;Caution<br>
    &nbsp;<i class="fa fa-circle" style="color:orange"></i>&nbsp;Extreme Caution<br>
    &nbsp;<i class="fa fa-circle" style="color:red"></i>&nbsp;Danger<br>
    &nbsp;<i class="fa fa-circle" style="color:darkred"></i>&nbsp;Extreme Danger<br>
    &nbsp;<i class="fa fa-circle" style="color:lightblue"></i>&nbsp;Not Available
    </div>
'''

# Create a Folium element from the legend HTML
legend = folium.Element(legend_html)
m.get_root().html.add_child(legend)

   
# If a specific city is selected, zoom to that city
if selected_city != 'Select City':
    m.location = city_coordinates[selected_city]
    m.zoom_start = 10

    # Filter the data based on the selected city
    filtered_df = filter_city_data(df, selected_city)
    #print(filtered_df)
    weather_df = get_weather_data_for_localities(filtered_df)
    
    if weather_df.empty:
        st.error('Unable to fetch data from API. Please try again later.')
    else:
        # Extract specific fields from locality_weather_data dictionary
        weather_df['temperature'] = weather_df['locality_weather_data'].apply(lambda x: x.get('temperature', None))
        weather_df['humidity'] = weather_df['locality_weather_data'].apply(lambda x: x.get('humidity', None))
        weather_df['wind_speed'] = weather_df['locality_weather_data'].apply(lambda x: x.get('wind_speed', None))
            
        # Drop the original 'locality_weather_data' column
        weather_df.drop(columns=['locality_weather_data'], inplace=True)
        
        # Drop rows where temperature or humidity is NaN
        weather_df.dropna(subset=['temperature', 'humidity'], inplace=True)
        
        #Merge the weather data with the original filtered DataFrame
        merged_df = pd.merge(filtered_df, weather_df, on='localityId')

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
        
        conditions = generate_conditions(merged_df)
        merged_df['feels_like'] = np.select(conditions, choices, default=None)
        merged_df['heat_index'] = merged_df.apply(lambda row: determine_heat_index(row['temperature'], row['humidity'])
                                              if pd.notna(row['temperature']) and pd.notna(row['humidity']) else "N/A",
                                              axis=1)

        print(merged_df)                
        
        for idx, row in merged_df.iterrows():
            coords = [row['latitude'], row['longitude']]
            popup_content = f"Feels Like: {row['feels_like']}°C"
            locality_name = row.get('localityName', f"Location {idx+1}")
            heat_index = row.get('heat_index', 'Default')  # Get heat_index from the DataFrame
            marker_color = get_marker_color(heat_index)  # Determine marker color based on heat_index
            
            folium.Marker(
                location=coords,
                popup=popup_content,
                tooltip=locality_name,
                icon=folium.Icon(color=marker_color)
                ).add_to(m)
        

        heat_data = [[row['latitude'], row['longitude'], row['feels_like']] for index, row in merged_df.iterrows()]

        # Define your fixed minimum and maximum 'feels_like' temperatures
        min_feels_like = 26
        max_feels_like = 43

        # Define your colormap with fixed range and colors
        colormap = cm.LinearColormap(colors=['blue','lightgreen', 'green', 'orange', 'red','darkred'],
                             vmin=min_feels_like, vmax=max_feels_like,
                             caption='Feels Like Temperature')
        
        min_opacity = 0.8
        radius = 50
        blur = 10

        # Define the range of feels_like values
        min_feels_like = merged_df['feels_like'].min()
        max_feels_like = merged_df['feels_like'].max()

        # Define your gradient based on feels_like values
        gradient = {
            0.0: 'blue',
            0.5: 'green',
            0.8: 'yellow',
            0.9: 'orange',
            1.0: 'red'
            }
    
        normalized_data = [[row[0], row[1], (row[2] - min_feels_like) / (max_feels_like - min_feels_like)] for row in heat_data]
        heatmap = HeatMap(normalized_data, min_opacity=min_opacity, radius=radius, blur=blur,gradient=gradient)
        heatmap_group = folium.FeatureGroup(name='Heat Map')
        heatmap_group.add_child(heatmap)
        m.add_child(heatmap_group)
        colormap.add_to(m)
    
        # Fetch and add public hospital data based on city bounding box
        bbox = get_bounding_box(city_coordinates[selected_city])
    
        # Define tags and icons for additional OSM layers
        amenities = {
            "Hospital":{"tag": "amenity=hospital", "icon": "hospital"},
            "Community Centres": {"tag": "amenity=community_centre", "icon": "home"},
            "Drinking Water": {"tag": "amenity=drinking_water", "icon": "tint"},
            "Parks": {"tag": "leisure=park", "icon": "tree"},
            "Gardens": {"tag": "leisure=garden", "icon": "leaf"},
            "Clinics": {"tag": "amenity=clinic", "icon": "plus-square"},
            "Pharmacies": {"tag": "amenity=pharmacy", "icon": "medkit"}
            }

        # Fetch and add each amenity as a different layer
        for amenity_name, amenity_info in amenities.items():
            tag = amenity_info["tag"]
            icon = amenity_info["icon"]
            osm_data = fetch_osm_data(bbox, [tag])
            
            # Logging to check fetched additional OSM data
            #print(f"Fetched {amenity_name} Data:", osm_data)

            amenity_group = folium.FeatureGroup(name=amenity_name, show=False)
           
            for element in osm_data.get('elements', []):
                lat = element.get('lat')
                lon = element.get('lon')
                if lat and lon:
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"{amenity_name}: {element['tags'].get('name', 'N/A')}",
                        icon=folium.Icon(color='blue', icon=icon)
                        ).add_to(amenity_group)
                   
            m.add_child(amenity_group)

        # Add LayerControl to the map
        folium.LayerControl().add_to(m)
    
        # Filter out locations with high temperatures
        temperature_threshold = 35  # Define your temperature threshold
        high_temp_locations = merged_df[merged_df['feels_like'] > temperature_threshold]
        
        st.sidebar.header("Route Finder")
        # Sidebar inputs for start and end location

        with st.sidebar:
            start_location = st_searchbox(get_location_suggestions, placeholder="Start Location", key="start_location")
            end_location = st_searchbox(get_location_suggestions, placeholder="End Location", key="end_location")
            calculate_route = st.sidebar.button("Calculate Route")
    
            # Get coordinates for start and end locations
            if calculate_route:
                start_coords = geocode_location(start_location)
                end_coords = geocode_location(end_location)
    
                if not start_coords or not end_coords:
                    st.sidebar.error("Could not find coordinates for one or both locations. Please try different place names.")
                else:
                    api_key = '5b3ce3597851110001cf624852bc21a822034504a103585fcd59c3f2'  # Replace with your actual OpenRouteService API key
                    original_route = get_route(start_coords, end_coords, api_key)
                
                    if original_route:
                        if route_passes_high_temp(original_route, high_temp_locations):
                            st.sidebar.warning("The original route passes through areas with high temperatures. Calculating alternative route...")
                    
                            # Attempt to calculate an alternative route that avoids high-temperature areas
                            alternative_route = None
                            for _, location in high_temp_locations.iterrows():
                                new_start_coords = (location['latitude'], location['longitude'])
                                new_end_coords = end_coords
                                alternative_route = get_route(new_start_coords, new_end_coords, api_key)
                    
                                if alternative_route and not route_passes_high_temp(alternative_route, high_temp_locations):
                                    st.sidebar.success("Alternative route found and displayed.")
                                    original_route = alternative_route
                                    break
                
                            if not alternative_route:
                                st.sidebar.error("Could not find an alternative route that avoids high-temperature areas. Displaying original route with warnings.")
                
                        # Display the route on the map
                        folium.Marker(location=start_coords, popup=start_location, icon=folium.Icon(color='green')).add_to(m)
                        folium.Marker(location=end_coords, popup=end_location, icon=folium.Icon(color='red')).add_to(m)
                        folium.PolyLine(original_route, color='blue', weight=5, opacity=0.8).add_to(m)
                    else:    
                        st.sidebar.error("Could not fetch the route for the provided locations. Please try again.")
    
    
# Render the map using components.html
map_html = m._repr_html_()
components.html(map_html, height=500, width= 1000)
weather_df = pd.DataFrame(weather_data_list)

# Check if weather_df is empty
if weather_df.empty:
    st.error('Unable to fetch data from API. Please try again later.')
else:
    
    conditions = generate_conditions(weather_df)

    choices = [weather_df['temperature'], 
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

    # Apply conditions to create a new column in the DataFrame
    weather_df['feels_like'] = np.select(conditions, choices, default=None)
   

if selected_city != 'Select City' and not weather_df.empty:
    styled_df = merged_df.copy()
    merged_df['feels_like'] = pd.to_numeric(merged_df['feels_like'], errors='coerce')
    feels_like_list = merged_df['feels_like'].tolist()
    styled_df['heat_index'] = merged_df.apply(
        lambda row: determine_heat_index(row['temperature'], row['humidity'])
        if pd.notna(row['temperature']) and pd.notna(row['humidity']) else "N/A",
        axis=1
    )
    styled_df_new = styled_df.drop(['cityName','localityId','latitude','longitude','temperature', 'humidity', 'feels_like' , 'device_type_x','device_type_y','status','message','wind_speed'], axis=1)
    # Create a container for the layout
    container = st.container()

    # Divide the container into a 2x2 grid using columns
    col1, col2 = container.columns(2)

    # Render styled dataframe in the first column
    with col1:
        st.write("### REAL FEEL")
        # Apply the color mapping to the DataFrame
        styled_df = styled_df_new.style.map(color_heat_index, subset=['heat_index'])
        # Display the DataFrame in the placeholder
        st.dataframe(styled_df,hide_index=True)
    
    # Line Chart for Temperature and Feels Like Temperature in the second row, first column
    long_df = pd.melt(merged_df, id_vars=['localityName'], value_vars=['temperature', 'feels_like'], var_name='Metric', value_name='Value')
    fig_line = px.line(
        long_df,
        x='localityName',
        y='Value',
        color='Metric',
        labels={'Value': 'Temperature (°C)', 'Metric': 'Metric'},
        markers=True
    )
    with col1:
        st.write("### Line Chart for Temperature and Feels Like Temperature - Temperature vs. Feels Like: What's the Difference?")
        st.plotly_chart(fig_line)
    

    with col2:
        st.write("### Scatter Plot for Temperature vs. Humidity - Temperature vs. Humidity: What's the Connection?")
        scatter_chart = px.scatter(
            merged_df,
            x='temperature',
            y='humidity',
            color='localityName',
            size=feels_like_list,
            labels={'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'},
            hover_data={'heat_index': True},  # Correct column name and ensure it's a dictionary
            )
        st.plotly_chart(scatter_chart)
        
        
if not weather_df.empty:
    placeholder = st.empty()

    weather_df_new = weather_df.drop(['temperature', 'humidity', 'feels_like'], axis=1)

    # Apply the color mapping to the dataframe
    styled_df = weather_df_new.style.map(color_heat_index, subset=['Heat Index'])

    # Ensure the 'feels_like' column is numeric
    weather_df['feels_like'] = pd.to_numeric(weather_df['feels_like'], errors='coerce')

    # Transform data to long format for line chart
    long_df = pd.melt(weather_df, id_vars=['City'], value_vars=['temperature', 'feels_like'],
                  var_name='Metric', value_name='Value')

    # Create a container for the layout
    container = st.container(height=None, border=None)

    # Divide the container into a 2x2 grid using columns
    col1, col2 = st.columns(2)


    # Render styled dataframe in the first row, first column
    with col1:
        st.write("### REAL FEEL")
        st.dataframe(styled_df,hide_index=True)

    # Line Chart for Temperature and Feels Like Temperature in the second row, first column
    long_df = pd.melt(weather_df, id_vars=['City'], value_vars=['temperature', 'feels_like'], var_name='Metric', value_name='Value')
    with col1:
        st.write("Line Chart for Temperature and Feels Like Temperature - Temperature vs. Feels Like: What's the Difference?")
        fig_line = px.line(
            long_df,
            x='City',
            y='Value',
            color='Metric',
            labels={'Value': 'Temperature (°C)', 'Metric': 'Metric'},
            markers=True
            )
        st.plotly_chart(fig_line)

    
    with col2:
        st.write("### Scatter Plot for Temperature vs. Humidity - Temperature vs. Humidity: What's the Connection?")
        # Scatter Plot for Temperature vs. Humidity in the second row, second column
        fig_scatter = px.scatter(
            weather_df,
            x='temperature',
            y='humidity',
            color='City',
            size='feels_like',
            labels={'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'},
            hover_data=['Heat Index']
            )
        st.plotly_chart(fig_scatter)
        
        
# Displaying logos and thank you message in the sidebar
st.sidebar.title('Acknowledgements')
st.sidebar.markdown('We have used APIs from the following services:')

# Inserting logos and thank you message
st.sidebar.image('https://www.weatherunion.com/_next/static/media/weatherunion-logo-dark.f6ef7a59.svg', width=200)
st.sidebar.image('https://openrouteservice.org/dev/static/img/logo@2x.1368651.png', width=200)
st.sidebar.markdown('**Thank you for providing valuable data!**')        

with st.expander("About Geo-Heat Shield: A Geospatial Approach to Heatwave Resilience Web App"):
    st.write("""Geo-Heat Shield is a web application designed to visualize and analyze weather data, focusing on heat index values across major cities in India. It fetches near real-time weather data, calculates heat indexes, and displays them on an interactive map. Users can explore detailed city-specific analyses, view temperature and humidity charts, and calculate safe travel routes based on temperature conditions. The app also integrates data on amenities like hospitals, community centres, drinking water points, parks, gardens, clinics, and pharmacies from OpenStreetMap to enhance user experience and safety. The app aims to enhance heatwave resilience by providing actionable insights and visualizations.""")
              
with st.expander("GeoFusionaires"):
    st.write("**Tej Chavda**")
    st.write("Email: TejP400@gmail.com")
    st.write("[LinkedIn](https://www.linkedin.com/in/tej-chavda/)")

    st.write("**Chancy Shah**")
    st.write("Email: shahchancy28@gmail.com")
    st.write("[Website](https://sites.google.com/view/chancyshah/profile)")
    st.write("[LinkedIn](https://www.linkedin.com/in/chancy-shah/)")
