from pydantic import BaseModel


class CurrentUnits(BaseModel):
    time: str
    interval: str
    temperature_2m: str
    precipitation: str
    rain: str
    showers: str
    is_day: str
    apparent_temperature: str
    relative_humidity_2m: str


class Current(BaseModel):
    time: str
    interval: int
    temperature_2m: float
    precipitation: float
    rain: float
    showers: float
    is_day: int
    apparent_temperature: float
    relative_humidity_2m: float


class Forecast(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_units: CurrentUnits
    current: Current