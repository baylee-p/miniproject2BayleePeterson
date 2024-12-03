# INF601 - Advanced Programming in Python
# Baylee Peterson
# Mini Project 2

import os
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Constants
API_KEY = "230df5d4a2d84be387a00929240312" # Replace with your API Key
BASE_URL = "http://api.weatherapi.com/v1/history.json"

# Function to fetch weather data
def fetch_weather_data(city, date):
    params = {
        "key": API_KEY,
        "q": city,
        "dt": date # Format: YYYY-MM-DD
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.json())
        return None

# Test fetching data
'''if __name__ == "__main__":
    city = "New York City"
    date = "2024-11-01"
    data = fetch_weather_data(city, date)
    if data:
        print(data)'''

# Process the data into a Pandas DataFrame
def process_weather_data(data):
    # Extract relevant information
    forecast = data['forecast']['forecastday'][0]
    date = forecast['date']
    avg_temp = forecast['day']['avgtemp_c']
    max_temp = forecast['day']['maxtemp_c']
    min_temp = forecast['day']['mintemp_c']

    # Create a DataFrame
    df = pd.DataFrame({
        "Date": [date],
        "Average Temp (°C)": [avg_temp],
        "Max Temp (°C)": [max_temp],
        "Min Temp (°C)": [min_temp]
    })
    return df

# Test processing
'''if __name__ == "__main__":
    city = "New York City"
    date = "2024-11-01"
    data = fetch_weather_data(city, date)
    if data:
        df = process_weather_data(data)
        print(df)'''

# List of cities
cities = ["New York City", "Los Angeles", "Chicago", "Austin", "Phoenix"]

# Dates in November
dates = pd.date_range("2024-11-01", "2024-11-07").strftime("%Y-%m-%d")

# Collect Data
all_data = []
for city in cities:
    for date in dates:
        data = fetch_weather_data(city, date)
        if data:
            df = process_weather_data(data)
            df['City'] = city
            all_data.append(df)

# Compile into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)
print(final_df)

# Plot average temperatures for each city
plt.figure(figsize=(12,6))
for city in cities:
    city_data = final_df[final_df['City'] == city]
    plt.plot(city_data["Date"], city_data["Average Temp (°C)"], label=city)

# Customize plot
plt.title("Average Temperatures from the first week of November 2024")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Create charts directory if does not exist
if not os.path.exists("charts"):
    os.makedirs("charts")

# Save the plot
plt.savefig("charts/average_temperatures.png")
plt.show()