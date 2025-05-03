import requests
from fastapi import FastAPI, Request, Query
from redis import Redis, RedisError
from typing import Any, Annotated
from .weather_values import Parameter, Current_Weather, GMT_MAP, CITIES_MAP
import json

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore
redis = Redis(host='redis', port=6379, decode_responses=True)

# Expires every hour
REDIS_EXPIRE_SECONDS = 60*60

def map_current_weather_options(temperature: bool, humidity: bool) -> str | None:
    """Map sunnyday API parameters that are equivalent to open-meteo API 'current weather'

    Args:
        temperature (bool): show temperature in API response
        humidity (bool): show humidity in API response

    Returns:
        str | None: list of open-meteo 'current weather' parameters separated by commas
    """    
    options: list[str] = []
    
    if temperature:
        options.append(Current_Weather.temperature.value)
    if humidity:
        options.append(Current_Weather.humidity.value)
        
    return ",".join(options) if options else None

def map_api_params(parameters: Annotated[Parameter, Query()]) ->  dict[str, Any]:
    """Maps parameters from sunnyday API to open-meteo API standard

    Args:
        parameters (Annotated[Parameter, Query): sunnyday API parameters

    Returns:
        dict[str, Any]: open-meteo standard parameters
    """   
    current_weather_options = map_current_weather_options(
        parameters.temperature, parameters.humidity
    )
    
    lat, lon = CITIES_MAP[parameters.city]
    
    open_meteo_params: dict[str, Any] = {
        "latitude": lat,
        "longitude": lon,
        "timezone": GMT_MAP[parameters.timezone]
    }
    
    if current_weather_options:
        open_meteo_params["current"] = current_weather_options
        
    return open_meteo_params

@app.get("/")
@limiter.limit("10/minute") # type: ignore
def root(request: Request, parameters: Annotated[Parameter, Query()]):
    
    cached_key = f"{parameters.city}:{parameters.timezone}:{parameters.temperature}:{parameters.humidity}"
    
    try:
        cached_response = redis.get(cached_key)
        if cached_response and isinstance(cached_response, str):
            return json.loads(cached_response)
    except RedisError as err:
        print(f"Redis error: {err}")
    
    open_meteo_params = map_api_params(parameters)
        
    try:
        response = requests.get('https://api.open-meteo.com/v1/forecast', params=open_meteo_params)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        return f"Connection error: {err}"
    
    try:
        redis.setex(name=cached_key, value=json.dumps(response.json()), time=REDIS_EXPIRE_SECONDS)
    except RedisError as err:
        print(f"Redis error: {err}")

    return response.json()