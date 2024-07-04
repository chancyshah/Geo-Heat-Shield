# Geo-Heat Shield: A Geospatial Approach to Heatwave Resilience

Geo-Heat Shield is a geospatial web application designed to visualize and analyze weather data, focusing on heat index values across major cities in India. It fetches near real-time weather data, calculates heat indexes, and displays them on an interactive map. Users can explore detailed city-specific analyses, view temperature and humidity charts, and calculate safe travel routes based on temperature conditions. The app aims to enhance heatwave resilience by providing actionable insights and visualizations.

## Table of Contents

- [Installation](#installation)
- [Running the Streamlit App](#running-the-streamlit-app)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Installation
Install Python 3.11 or higher.

Clone the repository

Navigate to the project directory: 
```bash
cd Geo-Heat-Shield
```
To install the necessary dependencies, run the following command:
```bash
pip install -r requirements.txt
```
## Running the Streamlit App
Follow these steps to run the Geo-Heat Shield Streamlit application:

Navigate to the Project Directory: Open your terminal or command prompt and change directory to where your project files (App.py, requirements.txt, etc.) are located.

Activate Virtual Environment (Optional): If you're using a virtual environment, activate it using:
```bash
source venv/bin/activate  
```
Run the Streamlit App: Start the Streamlit app by executing the following command:
```bash
streamlit run App.py
```
Open the Application: Streamlit will launch a local server and provide a URL (usually http://localhost:8501). Open this URL in your web browser to access the Geo-Heat Shield application.

Explore the Application: Use the interface provided by Streamlit to interact with the Geo-Heat Shield application.

Close the Application: To stop the Streamlit server, press Ctrl + C in your terminal.

## Acknowledgements

Special thanks to the following services for providing valuable data:

![Weather Union Logo](image/weatherunion-logo.png)  
**Weather Union**: Provides weather data services.

![OpenRouteService Logo](image/openrouteservice-logo.png)  
**OpenRouteService**: Offers routing and mapping services.

![Streamlit Logo](image/streamlit-logo.png)  
**Streamlit**: Powers the interactive app interface.

![OpenStreetMap Logo](image/Openstreetmap_logo.png)  
**OpenStreetMap**: Provides map data for visualizations and analysis.

Thank you all for providing valuable data and tools!


## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

**License Summary:**

- **BY**: Attribution is required, credit must be given to the creator.
- **NC**: NonCommercial uses only. Only noncommercial uses of the work are permitted.

You are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material.

Under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial**: You may not use the material for commercial purposes.

![CC BY-NC](image/by-nc.png)
