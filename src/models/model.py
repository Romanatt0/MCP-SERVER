from typing import Optional

from pydantic import BaseModel


class BaseForecast(BaseModel):
    """Campos comuns a todas as respostas da Open-Meteo."""

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float


# ---------- Tempo atual (parâmetro `current`) ----------

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


class Forecast(BaseForecast):
    current_units: CurrentUnits
    current: Current


# ---------- Previsão diária (parâmetro `daily`) ----------

class DailyUnits(BaseModel):
    time: str
    weather_code: str
    temperature_2m_max: str
    temperature_2m_min: str
    precipitation_sum: str
    precipitation_probability_max: str


class Daily(BaseModel):
    # A API devolve uma lista por variável, um item por dia.
    # Alguns valores podem vir null em dias mais distantes.
    time: list[str]
    weather_code: list[Optional[int]]
    temperature_2m_max: list[Optional[float]]
    temperature_2m_min: list[Optional[float]]
    precipitation_sum: list[Optional[float]]
    precipitation_probability_max: list[Optional[int]]


class DailyForecast(BaseForecast):
    daily_units: DailyUnits
    daily: Daily
