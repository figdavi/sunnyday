# sunnyday
A simple weather API that returns temperature and humidity for famous cities.

Built on top of [open-meteo](https://open-meteo.com/) with [FastAPI](https://fastapi.tiangolo.com/) and [Redis](https://redis.io/) for caching.

## How to run locally
1. Clone the repository
2. Run `cd sunnyday/`
3. Run `docker compose up --build -d`

## Example usage
Check temperature and humidity in New York:

`http://127.0.0.1:8000/?city=NYC`


```json
{
    "latitude":-36.875,
    "longitude":174.75,
    "generationtime_ms":0.021696090698242188,
    "utc_offset_seconds":0,
    "timezone":"GMT",
    "timezone_abbreviation":"GMT",
    "elevation":36.0,
    "current_units":
        {
            "time":"iso8601",
            "interval":"seconds",
            "temperature_2m":"°C",
            "relative_humidity_2m":"%"
        },
    "current":
        {
            "time":"2025-05-03T19:30",
            "interval":900,
            "temperature_2m":12.9,
            "relative_humidity_2m":81
        }
}
```

### Parameters
All parameters are based on the class `Parameters` in "[src\sunnyday\weather_values.py](src\sunnyday\weather_values.py)"

```python
class Parameter(BaseModel):
    city: CITIES
    timezone: TIMEZONES = "GMT0" 
    temperature: bool = True
    humidity: bool = True
```
You may optionally edit `timezone`, as well as `temperature` and `humidity`, to show 'temperature_2m' and 'relative_humidity_2m', respectively.

Example (timezone GMT12, show temperature and don't show humidity): 
`http://127.0.0.1:8000/?city=NYC&timezone=GMT12&temperature=true&humidity=false`

#### Paramameters `timezone` and `city` type (present in "src\sunnyday\weather_values.py")

```python 
TIMEZONES = Literal[
    "GMT-8",  # Anchorage, USA
    "GMT-7",  # Los Angeles, USA
    "GMT-6",  # Denver, USA
    "GMT-5",  # Chicago, USA
    "GMT-4",  # New York, USA
    "GMT-3",  # São Paulo, Brazil
    "GMT0",   # Greenwich, UK
    "GMT1",   # London, UK
    "GMT2",   # Berlin, Germany
    "GMT3M",  # Moscow, Russia
    "GMT3C",  # Cairo, Egypt
    "GMT7",   # Bangkok, Thailand
    "GMT8",   # Singapore
    "GMT9",   # Tokyo, Japan
    "GMT10",  # Sydney, Australia
    "GMT12"   # Auckland, New Zealand
]

CITIES = Literal[
    "NYC",  # New York, USA
    "LA",   # Los Angeles, USA
    "CHI",  # Chicago, USA
    "LON",  # London, UK
    "BER",  # Berlin, Germany
    "PAR",  # Paris, France
    "TOK",  # Tokyo, Japan
    "SYD",  # Sydney, Australia
    "SP",   # São Paulo, Brazil
    "CPT",  # Cape Town, South Africa
    "MOS",  # Moscow, Russia
    "BKK",  # Bangkok, Thailand
    "SG",   # Singapore
    "AKL",  # Auckland, New Zealand
]
```
