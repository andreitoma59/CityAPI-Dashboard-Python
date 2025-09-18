import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox,
    QLineEdit, QRadioButton, QButtonGroup, QHBoxLayout, QListWidget, QMessageBox, QMainWindow, QFrame, QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QColor, QPainter, QFont, QPalette, QLinearGradient, QBrush

load_dotenv()

IQ_AIR_API_KEY = os.getenv("IQ_AIR_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
GEO_API_KEY = os.getenv("GEO_API_KEY")
RESTAURANTS_API_KEY = os.getenv("RESTAURANTS_API_KEY")
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
IP_LOCATION_API_KEY = os.getenv("IP_LOCATION_API_KEY")

AQI_LEVELS = [
    (0, 50, QColor(0, 228, 0), "Bun"),
    (51, 100, QColor(255, 255, 0), "Moderat"),
    (101, 150, QColor(255, 126, 0), "Parțial Nesănătos"),
    (151, 200, QColor(255, 0, 0), "Nesănătos"),
    (201, 300, QColor(143, 63, 151), "Foarte Nesănătos"),
    (301, 500, QColor(126, 0, 35), "Periculos")
]

UV_LEVELS = [
    (0, 2, QColor(0, 255, 0), "Scăzut"),
    (3, 5, QColor(255, 255, 0), "Moderat"),
    (6, 7, QColor(255, 165, 0), "Ridicat"),
    (8, 10, QColor(255, 0, 0), "Foarte Ridicat"),
    (11, 15, QColor(128, 0, 128), "Extrem")
]

APP_STYLESHEET = """
    QWidget {
        font-family: 'Arial';
        font-size: 14px;
        background-color: #2E3440;
        color: #ECEFF4;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit {
        padding: 5px;
        border: 1px solid #4C566A;
        border-radius: 5px;
        background-color: #3B4252;
        color: #ECEFF4;
    }
    QGroupBox {
        border: 1px solid #4C566A;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 15px;
        font-weight: bold;
        background-color: #3B4252;
        color: #ECEFF4;
    }
    QListWidget {
        border: 1px solid #4C566A;
        border-radius: 5px;
        background-color: #3B4252;
        color: #ECEFF4;
    }
    QLabel {
        color: #ECEFF4;
    }
    QRadioButton {
        color: #ECEFF4;
    }
    QComboBox {
        background-color: #3B4252;
        color: #ECEFF4;
        border: 1px solid #4C566A;
        border-radius: 5px;
        padding: 5px;
    }
    QComboBox QAbstractItemView {
        background-color: #3B4252;
        color: #ECEFF4;
    }
    QLabel#emojiLabel {
        font-family: 'Apple Color Emoji';
        font-size: 42px;
    }
     QLabel#weatherLabel {
        font-size: 42px;
    }
"""
#API 1
def get_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea IP: {e}")
        return None
#API 2
def get_geo_info(ip):
    url = "https://ip-location5.p.rapidapi.com/get_geo_info"
    headers = {
        "x-rapidapi-key": "IP_LOCATION_API_KEY",
        "x-rapidapi-host": "ip-location5.p.rapidapi.com",
    }
    try:
        response = requests.post(url, data={"ip": ip}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea informațiilor geografice: {e}")
        return None
#API3
def get_city_info(city):
    encoded_city = requests.utils.quote(city)
    geo_url = f"https://geocode.maps.co/search?q={encoded_city}&api_key={GEO_API_KEY}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        if data:
            lat, lon = data[0]["lat"], data[0]["lon"]
            country = data[0].get("display_name", "").split(",")[-1].strip()
            return lat, lon, country
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea informațiilor despre oraș: {e}")
    return "N/A", "N/A", "N/A"
#API4
def get_air_quality(lat, lon):
    url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={IQ_AIR_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data and "current" in data["data"]:
            return data["data"]["current"]["pollution"]["aqius"]
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea calității aerului: {e}")
    return "N/A"
#API5
def get_exchange_rates(currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("conversion_rates", {})
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea ratelor de schimb: {e}")
        return {}
#API6
def get_currency_from_country(country):
    if country == "N/A":
        return "N/A"

    url = f"https://restcountries.com/v3.1/name/{country}?fields=currencies"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and "currencies" in data[0]:
        return list(data[0]["currencies"].keys())[0]
    return "N/A"
#API7
def get_weather_data(city):
    url = f"https://wttr.in/{city}?format=%t+%C+%c+%h+%u+%P"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            parts = response.text.strip().split()
            if len(parts) == 7:
                temp = parts[0]
                condition = f"{parts[1]} {parts[2]}"
                emoji = parts[3]
                humidity = parts[4]
                uv_index = parts[5]
                pressure = parts[6]
                return temp, condition, emoji, humidity, uv_index, pressure
            elif len(parts) == 6:
                temp, condition, emoji, humidity, uv_index, pressure = parts
                return temp, condition, emoji, humidity, uv_index, pressure
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea datelor meteo: {e}")
    return "N/A", "N/A", "❓", "N/A", "N/A", "N/A"

def get_clothing_recommendation(temp, condition):
    try:
        temp_value = float(temp.replace("°C", "").replace("°F", ""))
    except ValueError:
        return "N/A"

    if temp_value < 0:
        clothing = "Haină foarte groasă, mănuși, fular și pălărie. Îmbrăcați-vă bine!"
    elif 0 <= temp_value < 10:
        clothing = "Haină groasă, pulover și pantaloni lungi. Este frig!"
    elif 10 <= temp_value < 20:
        clothing = "Geacă subțire sau pulover. Este răcoare."
    elif 20 <= temp_value < 30:
        clothing = "Tricou și pantaloni scurți sau haine ușoare. Este cald."
    else:
        clothing = "Haine ușoare și respirabile. Este foarte cald!"

    if "rain" in condition.lower():
        clothing += " Nu uitați de umbrelă sau pelerină!"
    elif "snow" in condition.lower():
        clothing += " Încălțăminte impermeabilă și straturi groase."
    # elif "sun" in condition.lower() or "clear" in condition.lower():
    elif "sun" in condition.lower() :
        clothing += " Purtați ochelari de soare și aplicați cremă de protecție solară."

    return clothing
#API8
def get_nearby_restaurants(lat, lon):
    url = f"https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:{lon},{lat},500&bias=proximity:{lon},{lat}&limit=20&apiKey={RESTAURANTS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "features" in data:
            return data["features"]
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea restaurantelor: {e}")
    return []
#API9
def get_current_time_by_coordinates(lat, lon, username=GEONAMES_USERNAME):
    url = "http://api.geonames.org/timezoneJSON"
    params = {
        "lat": lat,
        "lng": lon,
        "username": username,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "time" in data:
            time_str = data["time"]
            date, time = time_str.split(" ")
            return f"Dată: {date}\nOra: {time}"
        else:
            print(f"Eroare: {data.get('message', 'Eroare necunoscută')}")
            return "N/A"
    except requests.exceptions.RequestException as e:
        print(f"Eroare la obținerea orei curente: {e}")
        return "N/A"

class AQIBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.aqi_value = 0

    def set_aqi(self, value):
        self.aqi_value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        section_width = width // len(AQI_LEVELS)
        for i, (min_val, max_val, color, _) in enumerate(AQI_LEVELS):
            painter.setBrush(color)
            painter.drawRect(i * section_width, 0, section_width, height)

        if self.aqi_value != "N/A":
            pos = min(max(self.aqi_value, 0), 500) / 500 * width
            painter.setBrush(Qt.white)
            painter.drawEllipse(int(pos) - 5, height // 2 - 5, 10, 10)

class UVBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uv_value = 0

    def set_uv(self, value):
        self.uv_value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        section_width = width // len(UV_LEVELS)
        for i, (min_val, max_val, color, _) in enumerate(UV_LEVELS):
            painter.setBrush(color)
            painter.drawRect(i * section_width, 0, section_width, height)

        if self.uv_value != "N/A":
            pos = min(max(self.uv_value, 0), 15) / 15 * width
            painter.setBrush(Qt.white)
            painter.drawEllipse(int(pos) - 5, height // 2 - 5, 10, 10)

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proiect TAD 1")
        self.showMaximized()

        self.setStyleSheet(APP_STYLESHEET)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, 60)

        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout, 40)

        self.map_frame = QFrame()
        self.map_frame.setFrameShape(QFrame.StyledPanel)
        self.right_layout.addWidget(self.map_frame)

        self.map_view = QWebEngineView()
        self.map_layout = QVBoxLayout(self.map_frame)
        self.map_layout.addWidget(self.map_view)

        self.location_group = QGroupBox("Setări Locație")
        self.location_layout = QVBoxLayout()
        self.auto_radio = QRadioButton("Folosește Adresa IP")
        self.manual_radio = QRadioButton("Introduceți Orașul")
        self.auto_radio.setChecked(True)

        self.location_layout.addWidget(self.auto_radio)
        self.location_layout.addWidget(self.manual_radio)

        self.get_ip_button = QPushButton("Obține IP-ul Dispozitivului")
        self.get_ip_button.clicked.connect(self.get_ip_and_update)

        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("Introduceți Numele Orașului")
        self.city_button = QPushButton("Caută Coordonate")
        self.city_button.clicked.connect(self.get_city_details)

        self.coordinates_label = QLabel("Coordonate: -")
        self.coordinates_label.setAlignment(Qt.AlignCenter)

        self.location_layout.addWidget(self.get_ip_button)
        self.location_layout.addWidget(self.city_entry)
        self.location_layout.addWidget(self.city_button)
        self.location_layout.addWidget(self.coordinates_label)
        self.location_group.setLayout(self.location_layout)
        self.left_layout.addWidget(self.location_group)

        self.aqi_uv_group = QGroupBox("Calitatea Aerului & Index UV")
        self.aqi_uv_layout = QVBoxLayout()

        self.aqi_bar = AQIBar()
        self.aqi_bar.setFixedHeight(30)
        self.aqi_uv_layout.addWidget(self.aqi_bar)

        self.aqi_labels_layout = QHBoxLayout()
        self.aqi_labels = []
        for _, _, color, text in AQI_LEVELS:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()});")
            self.aqi_labels.append(label)
            self.aqi_labels_layout.addWidget(label)
        self.aqi_uv_layout.addLayout(self.aqi_labels_layout)

        self.aqi_label = QLabel("AQI: -")
        self.aqi_label.setAlignment(Qt.AlignCenter)
        self.aqi_uv_layout.addWidget(self.aqi_label)

        self.uv_bar = UVBar()
        self.uv_bar.setFixedHeight(30)
        self.aqi_uv_layout.addWidget(self.uv_bar)

        self.uv_labels_layout = QHBoxLayout()
        self.uv_labels = []
        for _, _, color, text in UV_LEVELS:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()});")
            self.uv_labels.append(label)
            self.uv_labels_layout.addWidget(label)
        self.aqi_uv_layout.addLayout(self.uv_labels_layout)

        self.uv_index_label = QLabel("Index UV: -")
        self.uv_index_label.setAlignment(Qt.AlignCenter)
        self.aqi_uv_layout.addWidget(self.uv_index_label)

        self.aqi_uv_group.setLayout(self.aqi_uv_layout)
        self.left_layout.addWidget(self.aqi_uv_group)

        self.currency_group = QGroupBox("Conversie Valutară")
        self.currency_layout = QVBoxLayout()

        self.currency_var = QComboBox()
        self.currency_var.currentIndexChanged.connect(self.update_exchange_rate)
        self.currency_layout.addWidget(self.currency_var)

        self.rate_label = QLabel("Selectați o Valută")
        self.rate_label.setAlignment(Qt.AlignCenter)
        self.currency_layout.addWidget(self.rate_label)

        self.update_button = QPushButton("Actualizează")
        self.update_button.clicked.connect(self.update_exchange_rate)
        self.currency_layout.addWidget(self.update_button)

        self.currency_group.setLayout(self.currency_layout)
        self.left_layout.addWidget(self.currency_group)

        self.weather_group = QGroupBox("Vreme")
        self.weather_layout = QVBoxLayout()

        self.weather_display = QHBoxLayout()
        self.temperature_label = QLabel("N/A")
        self.temperature_label.setFont(QFont("Arial", 36))
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setObjectName("weatherLabel")

        self.weather_emoji = QLabel("❓")
        self.weather_emoji.setFont(QFont("Apple Color Emoji", 72))
        self.weather_emoji.setAlignment(Qt.AlignCenter)
        self.weather_emoji.setObjectName("emojiLabel")
        self.weather_display.addWidget(self.temperature_label)
        self.weather_display.addWidget(self.weather_emoji)
        self.weather_layout.addLayout(self.weather_display)

        self.weather_condition_label = QLabel("Condiții: -")
        self.weather_condition_label.setFont(QFont("Arial", 14))
        self.weather_condition_label.setAlignment(Qt.AlignCenter)
        self.weather_layout.addWidget(self.weather_condition_label)

        self.humidity_label = QLabel("Umiditate: -")
        self.humidity_label.setFont(QFont("Arial", 14))
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.weather_layout.addWidget(self.humidity_label)

        self.pressure_label = QLabel("Presiune: -")
        self.pressure_label.setFont(QFont("Arial", 14))
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.weather_layout.addWidget(self.pressure_label)

        self.clothing_label = QLabel("Recomandări de Îmbrăcăminte: -")
        self.clothing_label.setFont(QFont("Arial", 14))
        self.clothing_label.setAlignment(Qt.AlignCenter)
        self.weather_layout.addWidget(self.clothing_label)

        self.weather_group.setLayout(self.weather_layout)
        self.left_layout.addWidget(self.weather_group)

        self.current_time_group = QGroupBox("Ora Curentă Bazată pe Fusul Orar")
        self.current_time_layout = QVBoxLayout()

        self.current_time_label = QLabel("Dată: -\nOra: -")
        self.current_time_label.setAlignment(Qt.AlignCenter)
        self.current_time_layout.addWidget(self.current_time_label)

        self.current_time_group.setLayout(self.current_time_layout)
        self.left_layout.addWidget(self.current_time_group)

        self.restaurants_group = QGroupBox("Restaurante din Apropiere")
        self.restaurants_layout = QVBoxLayout()

        self.restaurant_list = QListWidget()
        self.restaurants_layout.addWidget(self.restaurant_list)

        self.restaurants_group.setLayout(self.restaurants_layout)
        self.left_layout.addWidget(self.restaurants_group)

        self.restaurants_data = []

        self.restaurant_list.itemClicked.connect(self.on_restaurant_clicked)

        self.auto_radio.toggled.connect(self.update_location_mode)
        self.manual_radio.toggled.connect(self.update_location_mode)

        self.update_location_mode()
        self.get_ip_and_update()

    def update_location_mode(self):
        if self.auto_radio.isChecked():
            self.location_layout.addWidget(self.get_ip_button)
            self.location_layout.removeWidget(self.city_entry)
            self.location_layout.removeWidget(self.city_button)
            self.city_entry.hide()
            self.city_button.hide()
            self.get_ip_button.show()
            self.get_ip_and_update()
        else:
            self.location_layout.addWidget(self.city_entry)
            self.location_layout.addWidget(self.city_button)
            self.location_layout.removeWidget(self.get_ip_button)
            self.city_entry.show()
            self.city_button.show()
            self.get_ip_button.hide()
            self.coordinates_label.setText("Coordonate: -")
            self.aqi_label.setText("AQI: -")
            self.aqi_bar.set_aqi(0)
            self.uv_index_label.setText("Index UV: -")
            self.uv_bar.set_uv(0)

    def get_ip_and_update(self):
        ip = get_ip()
        if not ip:
            QMessageBox.warning(self, "Eroare", "Nu s-a putut obține adresa IP.")
            return

        geo_info = get_geo_info(ip)
        if not geo_info:
            QMessageBox.warning(self, "Eroare", "Nu s-au putut obține informații de geolocalizare.")
            return

        self.city = geo_info.get("city")
        self.lat = geo_info.get("latitude", "46.7712")
        self.lon = geo_info.get("longitude", "23.6236")
        self.coordinates_label.setText(f"Coordonate: Lat {self.lat}, Lon {self.lon}")

        aqi = get_air_quality(self.lat, self.lon)
        self.aqi_label.setText(f"AQI: {aqi}")
        self.aqi_bar.set_aqi(int(aqi) if aqi != "N/A" else 0)

        self.update_map()
        self.update_weather(self.city)
        self.update_restaurants(self.lat, self.lon)

        base_currency = geo_info.get("country", {}).get("currency", "USD")
        self.exchange_rates = get_exchange_rates(base_currency)
        self.base_currency_var = base_currency
        self.currency_var.clear()
        self.currency_var.addItems(self.exchange_rates.keys())
        self.update_exchange_rate()

    def get_city_details(self):
        city = self.city_entry.text()
        if not city:
            QMessageBox.warning(self, "Eroare", "Vă rugăm să introduceți un nume de oraș valid.")
            return

        lat, lon, country = get_city_info(city)
        if lat == "N/A" or lon == "N/A":
            QMessageBox.warning(self, "Eroare", "Nu s-au putut obține coordonatele orașului.")
            return

        self.coordinates_label.setText(f"Coordonate: Lat {lat}, Lon {lon}")
        self.update_weather(city)

        aqi = get_air_quality(lat, lon)
        self.aqi_label.setText(f"AQI: {aqi}")
        self.aqi_bar.set_aqi(int(aqi) if aqi != "N/A" else 0)

        self.lat, self.lon = lat, lon
        self.update_map()
        self.update_restaurants(lat, lon)

        base_currency = get_currency_from_country(country)
        self.base_currency_var = base_currency
        self.exchange_rates = get_exchange_rates(base_currency)

        self.currency_var.clear()
        self.currency_var.addItems(self.exchange_rates.keys())
        self.update_exchange_rate()

    def update_map(self, lat=None, lon=None):
        if lat is None or lon is None:
            lat, lon = self.lat, self.lon
        map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon},{lat},{lon},{lat}&marker={lat},{lon}"
        self.map_view.setUrl(QUrl(map_url))

    def update_exchange_rate(self):
        selected_currency = self.currency_var.currentText()
        rate = self.exchange_rates.get(selected_currency, "N/A")
        self.rate_label.setText(f"1 {self.base_currency_var} = {rate} {selected_currency}")

    def update_weather(self, city):
        temp, condition, emoji, humidity, uv_index, pressure = get_weather_data(city)
        self.temperature_label.setText(temp)
        self.weather_emoji.setText(emoji)
        self.weather_condition_label.setText(f"Condiții: {condition}")
        self.humidity_label.setText(f"Umiditate: {humidity}")
        self.uv_index_label.setText(f"Index UV: {uv_index}")
        self.uv_bar.set_uv(int(uv_index) if uv_index != "N/A" else 0)
        self.pressure_label.setText(f"Presiune: {pressure}")

        clothing_recommendation = get_clothing_recommendation(temp, condition)
        self.clothing_label.setText(f"Recomandări de Îmbrăcăminte: {clothing_recommendation}")

        current_time = get_current_time_by_coordinates(self.lat, self.lon)
        self.current_time_label.setText(f"{current_time}")

    def update_restaurants(self, lat, lon):
        self.restaurant_list.clear()
        self.restaurants_data = get_nearby_restaurants(lat, lon)
        for restaurant in self.restaurants_data:
            name = restaurant["properties"].get("name", "N/A")
            address = restaurant["properties"].get("formatted", "N/A")
            cuisine = restaurant["properties"].get("catering", {}).get("cuisine", "N/A")
            self.restaurant_list.addItem(f"{address} - Specific: {cuisine}")

    def on_restaurant_clicked(self, item):
        index = self.restaurant_list.row(item)
        if 0 <= index < len(self.restaurants_data):
            restaurant = self.restaurants_data[index]
            lat = restaurant["geometry"]["coordinates"][1]
            lon = restaurant["geometry"]["coordinates"][0]
            self.update_map(lat, lon)

app = QApplication(sys.argv)
window = CurrencyConverter()
window.show()
sys.exit(app.exec_())