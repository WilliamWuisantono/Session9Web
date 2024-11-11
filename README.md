# Weather Dashboard

## Overview

This project is a weather dashboard built using Python, Flask, and Matplotlib. The objective is to retrieve weather data for a given city, process, and display various weather attributes. Weather attributes I chose besides temperature are humidity, dew point, and rainfall, and then graphically represent these attributes. The results are displayed on a web page, and the user can interact with the dashboard to view different weather forecasts for the city of their choice.

## Objectives

The goal of this assignment was to:

1. **Obtain and process three additional attributes** in the weather data:
   - Temperature
   - Humidity
   - Dew Point
   - Rainfall (precipitation)
   
2. **Graphically represent the additional attributes** using Matplotlib.

3. **Update the HTML template** to display the graphical data of these weather attributes.

## Features

- The user inputs a city name into a form to retrieve the weather forecast.
- The dashboard displays and graphs the following data for the next 24 hours:
  - Temperature (°C)
  - Humidity (%)
  - Dew Point (°C)
  - Rainfall (mm)

## File Structure

The project consists of the following files:

- `app.py`: The main Python script that runs the Flask web server, fetches weather data, generates plots, and serves the HTML template.
- `templates/weather.html`: The HTML template renders the weather data and graphs on the web page.
- `static/`: This directory contains the saved plot images (e.g., temperature, humidity, dew point, and rain graphs).

## Requirements
Libraries Used:
- Flask
- Matplotlib
- Requests
