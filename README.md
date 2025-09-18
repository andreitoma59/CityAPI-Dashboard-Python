# CityAPI Dashboard Python


This repository contains a comprehensive city information dashboard built with Python and PyQt5. The application fetches and displays a wide range of real-time data for any given location by aggregating information from nine different public APIs. It serves as a one-stop-shop for weather, air quality, local amenities, and more, presented in a clean, dark-themed graphical user interface.

## Features

-   **Dual Location Modes:** Automatically detect your location via public IP or manually search for any city worldwide.
-   **Interactive Map Display:** Shows the selected location on an embedded OpenStreetMap, which can also pinpoint specific points of interest like restaurants.
-   **Comprehensive Weather Data:** Get real-time temperature, weather conditions, humidity, atmospheric pressure, and UV index.
-   **Smart Clothing Recommendations:** Suggests appropriate attire based on current weather conditions (e.g., bring an umbrella for rain, wear sunscreen on sunny days).
-   **Air Quality & UV Index Monitoring:** Displays the Air Quality Index (AQI) and UV Index with color-coded bars for easy interpretation of environmental conditions.
-   **Local Time Display:** Automatically calculates and displays the current date and time for the selected coordinates' timezone.
-   **Currency Converter:** Fetches the local currency for the selected country and displays exchange rates against other major currencies.
-   **Nearby Restaurant Finder:** Lists restaurants within a 500m radius of the selected coordinates, including their address and cuisine type.

## APIs Used

This application integrates data from the following services:

-   **ipify:** For retrieving the user's public IP address.
-   **IP-Location (RapidAPI):** For geolocating an IP address to a city and country.
-   **Geocode Maps:** For converting city names into geographic coordinates.
-   **IQAir (AirVisual):** For real-time air quality data (AQI).
-   **ExchangeRate-API:** For currency conversion rates.
-   **REST Countries:** For identifying a country's official currency.
-   **wttr.in:** For detailed weather information and forecasts.
-   **Geoapify:** For finding nearby places of interest (restaurants).
-   **Geonames:** For timezone and local time data based on coordinates.

## Setup and Installation

Follow these steps to run the application on your local machine.

### 1. Prerequisites

-   Python 3.x
-   `pip` package manager

### 2. Clone the Repository

```bash
git clone https://github.com/andreitoma59/cityapi-dashboard-python.git
cd cityapi-dashboard-python
```

### 3. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install requests PyQt5 PyQtWebEngine python-dotenv
```

### 4. Configure API Keys

This project requires several API keys to function.

1.  Create a file named `.env` in the root directory of the project.
2.  Obtain the necessary API keys and credentials from the services listed in the "APIs Used" section.
3.  Add your keys to the `.env` file in the following format:

    ```env
    IQ_AIR_API_KEY="your_iq_air_key"
    EXCHANGE_API_KEY="your_exchangerate_api_key"
    GEO_API_KEY="your_geocode_maps_key"
    RESTAURANTS_API_KEY="your_geoapify_key"
    GEONAMES_USERNAME="your_geonames_username"
    IP_LOCATION_API_KEY="your_ip_location_rapidapi_key"
    ```

## Usage

To run the application, execute the `main.py` script from your terminal:

```bash
python main.py
```

-   The application will start in "Use IP Address" mode and attempt to auto-detect your location.
-   To search for a different city, select the "Enter City" radio button, type the city name in the input field, and click "Search Coordinates".
-   All data panels (Weather, AQI, Currency, etc.) will update automatically based on the selected location.
-   Click on a restaurant in the "Nearby Restaurants" list to pinpoint its location on the map.