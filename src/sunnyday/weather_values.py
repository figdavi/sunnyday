from typing import Literal
from enum import Enum
from pydantic import BaseModel

TIMEZONES = Literal[
    "GMT-8", "GMT-7", "GMT-6", "GMT-5", "GMT-4", "GMT-3",
    "GMT0", "GMT1", "GMT2", "GMT3M", "GMT3C",
    "GMT7", "GMT8", "GMT9", "GMT10", "GMT12",
]

GMT_MAP = {
    "GMT-8": "America/Anchorage",
    "GMT-7": "America/Los_Angeles",
    "GMT-6": "America/Denver",
    "GMT-5": "America/Chicago",
    "GMT-4": "America/New_York",
    "GMT-3": "America/Sao_Paulo",
    "GMT0": "GMT",
    "GMT1": "Europe/London",
    "GMT2": "Europe/Berlin",
    "GMT3M": "Europe/Moscow",
    "GMT3C": "Africa/Cairo",
    "GMT7": "Asia/Bangkok",
    "GMT8": "Asia/Singapore",
    "GMT9": "Asia/Tokyo",
    "GMT10": "Australia/Sydney",
    "GMT12": "Pacific/Auckland"
}

CITIES = Literal[
    "NYC", "LA", "CHI", "LON", "BER", "PAR","TOK", "SYD",
    "SP", "CPT", "MOS", "BKK", "SG", "AKL"
]

CITIES_MAP = {
    "NYC": (40.7128, -74.0060),      # New York, USA
    "LA": (34.0522, -118.2437),      # Los Angeles, USA
    "CHI": (41.8781, -87.6298),      # Chicago, USA
    "LON": (51.5074, -0.1278),       # London, UK
    "BER": (52.5200, 13.4050),       # Berlin, Germany
    "PAR": (48.8566, 2.3522),        # Paris, France
    "TOK": (35.6895, 139.6917),      # Tokyo, Japan
    "SYD": (-33.8688, 151.2093),     # Sydney, Australia
    "SP": (-23.5505, -46.6333),      # São Paulo, Brazil
    "CPT": (-33.9249, 18.4241),      # Cape Town, South Africa
    "MOS": (55.7558, 37.6173),       # Moscow, Russia
    "BKK": (13.7563, 100.5018),      # Bangkok, Thailand
    "SG": (1.3521, 103.8198),        # Singapore
    "AKL": (-36.8485, 174.7633),     # Auckland, New Zealand
}

class Current_Weather(Enum):
    temperature = "temperature_2m"
    humidity = "relative_humidity_2m"
    
class Parameter(BaseModel):
    city: CITIES
    timezone: TIMEZONES = "GMT0" 
    temperature: bool = True
    humidity: bool = True