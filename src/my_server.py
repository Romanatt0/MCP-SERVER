from datetime import date
from typing import Annotated

import requests
from fastmcp import FastMCP
from pydantic import Field, ValidationError

from models.model import DailyForecast, Forecast

# Coordenadas de Joinville - SC
LATITUDE = -26.3044
LONGITUDE = -48.8456
TIMEZONE = "America/Sao_Paulo"
API_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SEGUNDOS = 10

DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

# Códigos WMO usados pela Open-Meteo -> descrição em português
# https://open-meteo.com/en/docs (seção "WMO Weather interpretation codes")
WMO_CODES = {
    0: "céu limpo",
    1: "predominantemente limpo",
    2: "parcialmente nublado",
    3: "nublado",
    45: "neblina",
    48: "neblina com geada",
    51: "garoa fraca",
    53: "garoa moderada",
    55: "garoa intensa",
    56: "garoa congelante fraca",
    57: "garoa congelante intensa",
    61: "chuva fraca",
    63: "chuva moderada",
    65: "chuva forte",
    66: "chuva congelante fraca",
    67: "chuva congelante forte",
    71: "neve fraca",
    73: "neve moderada",
    75: "neve forte",
    77: "grãos de neve",
    80: "pancadas de chuva fracas",
    81: "pancadas de chuva moderadas",
    82: "pancadas de chuva fortes",
    85: "pancadas de neve fracas",
    86: "pancadas de neve fortes",
    95: "trovoada",
    96: "trovoada com granizo fraco",
    99: "trovoada com granizo forte",
}

mcp = FastMCP("MeuServidorMCP")
print(f"Servidor MCP '{mcp.name}' inicializado.")


def consultar_open_meteo(params: dict) -> dict:
    """Faz a requisição à Open-Meteo para Joinville e devolve o JSON."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE,
        **params,
    }
    response = requests.get(API_URL, params=params, timeout=TIMEOUT_SEGUNDOS)
    response.raise_for_status()
    return response.json()


def formatar_valor(valor, unidade: str) -> str:
    return "sem dados" if valor is None else f"{valor}{unidade}"


@mcp.tool(
    name="previsao_tempo_joinville",
    description=(
        "Retorna as condições do tempo AGORA em Joinville - SC: temperatura, "
        "sensação térmica, umidade e chuva. Use quando o usuário perguntar como "
        "está o clima, a temperatura ou se está chovendo neste momento em Joinville."
    ),
)
def previsao_tempo_joinville() -> str:
    try:
        data = consultar_open_meteo({
            "current": "temperature_2m,precipitation,rain,showers,is_day,"
                       "apparent_temperature,relative_humidity_2m",
        })
        forecast = Forecast.model_validate(data)
    except requests.RequestException as e:
        return f"Erro ao obter previsão do tempo: {e}"
    except ValidationError as e:
        return f"A API de clima retornou dados em formato inesperado: {e}"

    atual = forecast.current
    un = forecast.current_units
    periodo = "dia" if atual.is_day else "noite"

    return (
        f"Tempo atual em Joinville - SC ({atual.time.replace('T', ' ')}, {periodo}):\n"
        f"- Temperatura: {atual.temperature_2m}{un.temperature_2m} "
        f"(sensação de {atual.apparent_temperature}{un.apparent_temperature})\n"
        f"- Umidade relativa: {atual.relative_humidity_2m:.0f}{un.relative_humidity_2m}\n"
        f"- Precipitação: {atual.precipitation} {un.precipitation} "
        f"(chuva: {atual.rain} {un.rain}, pancadas: {atual.showers} {un.showers})"
    )


@mcp.tool(
    name="previsao_proximos_dias_joinville",
    description=(
        "Retorna a previsão do tempo dia a dia para Joinville - SC: condição do "
        "tempo, temperaturas mínima e máxima, chance de chuva e volume de chuva. "
        "Use quando o usuário perguntar sobre amanhã, os próximos dias, o fim de "
        "semana ou uma data futura em Joinville. O dia 1 é hoje."
    ),
)
def previsao_proximos_dias_joinville(
    dias: Annotated[
        int,
        Field(ge=1, le=16, description="Quantidade de dias a partir de hoje (1 a 16)."),
    ] = 7,
) -> str:
    try:
        data = consultar_open_meteo({
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                     "precipitation_sum,precipitation_probability_max",
            "forecast_days": dias,
        })
        forecast = DailyForecast.model_validate(data)
    except requests.RequestException as e:
        return f"Erro ao obter previsão do tempo: {e}"
    except ValidationError as e:
        return f"A API de clima retornou dados em formato inesperado: {e}"

    d = forecast.daily
    un = forecast.daily_units
    linhas = [f"Previsão para Joinville - SC nos próximos {dias} dia(s):"]

    for i, dia_iso in enumerate(d.time):
        data_dia = date.fromisoformat(dia_iso)
        codigo = d.weather_code[i]
        condicao = WMO_CODES.get(codigo, "sem dados") if codigo is not None else "sem dados"
        linhas.append(
            f"- {DIAS_SEMANA[data_dia.weekday()]} {data_dia:%d/%m}: {condicao}; "
            f"mín {formatar_valor(d.temperature_2m_min[i], un.temperature_2m_min)}, "
            f"máx {formatar_valor(d.temperature_2m_max[i], un.temperature_2m_max)}; "
            f"chance de chuva {formatar_valor(d.precipitation_probability_max[i], un.precipitation_probability_max)}, "
            f"volume {formatar_valor(d.precipitation_sum[i], ' ' + un.precipitation_sum)}"
        )

    return "\n".join(linhas)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
