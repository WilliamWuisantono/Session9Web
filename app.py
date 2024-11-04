import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
import requests
import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather():
    weather_data = None
    graph_filenames = None
    if request.method == 'POST':
        city = request.form['city']
        
        # Geocoding to get latitude and longitude for the city using Open-Meteo's location API
        geocoding_response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}')
        
        if geocoding_response.status_code == 200 and geocoding_response.json().get('results'):
            location = geocoding_response.json()['results'][0]
            latitude, longitude = location['latitude'], location['longitude']
            
            # Fetch hourly forecast data for temperature
            weather_response = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,rain&timezone=auto'
            )
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                graph_filenames = generate_temperature_graph(weather_data)
            else:
                weather_data = {'error': 'Unable to retrieve weather data.'}
        else:
            weather_data = {'error': 'City not found'}
            
    return render_template('weather.html', weather_data=weather_data, graph_filenames=graph_filenames)

def generate_temperature_graph(weather_data):
    # Parse hourly temperature data
    times = weather_data['hourly']['time'][:24]
    temperatures = weather_data['hourly']['temperature_2m'][:24]
    humidity = weather_data['hourly']['relative_humidity_2m'][:24]
    dew_point = weather_data['hourly']['dew_point_2m'][:24]
    rain = weather_data['hourly']['rain'][:24]

    time_labels = [datetime.datetime.fromisoformat(time).strftime('%H:%M') for time in times]
    # Ensure the static directory exists
    
    if not os.path.exists('static'):
        os.mkdir('static')

    # Plot and save each attribute separately
    graph_filenames = {}

    # Plot Temperature Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, temperatures, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Forecast for the Next 24 Hours')
    plt.tight_layout()
    temperature_filename = './static/temperature_plot.png'
    plt.savefig(temperature_filename)
    plt.close()
    graph_filenames['temperature'] = temperature_filename

    # Plot Humidity Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, humidity, marker='x', linestyle='-', color='g')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity Forecast for the Next 24 Hours')
    plt.tight_layout()
    humidity_filename = './static/humidity_plot.png'
    plt.savefig(humidity_filename)
    plt.close()
    graph_filenames['humidity'] = humidity_filename

    # Plot Dew-Point Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, dew_point, marker='^', linestyle='-', color='r')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Dew Point (°C)')
    plt.title('Dew Point Forecast for the Next 24 Hours')
    plt.tight_layout()
    dew_point_filename = './static/dew_point_plot.png'
    plt.savefig(dew_point_filename)
    plt.close()
    graph_filenames['dew_point'] = dew_point_filename

    # Plot Rain Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, rain, marker='s', linestyle='-', color='purple')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Rain (mm)')
    plt.title('Rain Forecast for the Next 24 Hours')
    plt.tight_layout()
    rain_filename = './static/rain_plot.png'
    plt.savefig(rain_filename)
    plt.close()
    graph_filenames['rain'] = rain_filename

    return graph_filenames


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.mkdir('static')
    app.run(debug=True)