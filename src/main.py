from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context
import requests


# 1. Inicialize o Servidor
mcp = FastMCP("MeuServidorMCP")     
print(f"Servidor MCP '{mcp.name}' inicializado.")

# 2. Defina a ferramenta de previsão do tempo para Joinville
@mcp.tool()
def previsao_tempo_joinville() -> str:
    """
    Ferramenta que obtém a previsão do tempo atual para Joinville.
    
    Returns:
        Uma string com os dados atuais do tempo em Joinville
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=-26.3044&longitude=-48.8456&current=temperature_2m,precipitation,rain,showers,is_day,apparent_temperature,relative_humidity_2m&forecast_days=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        current = data.get('current', {})
        temperature = current.get('temperature_2m', 'N/A')
        precipitation = current.get('precipitation', 'N/A')
        rain = current.get('rain', 'N/A')
        showers = current.get('showers', 'N/A')
        is_day = 'Dia' if current.get('is_day') else 'Noite'
        apparent_temperature = current.get('apparent_temperature', 'N/A')
        humidity = current.get('relative_humidity_2m', 'N/A')
        
        result = f"Previsão do tempo para Joinville:\n" \
                 f"Temperatura: {temperature}°C\n" \
                 f"Temperatura aparente: {apparent_temperature}°C\n" \
                 f"Precipitação: {precipitation} mm\n" \
                 f"Chuva: {rain} mm\n" \
                 f"Pancadas: {showers} mm\n" \
                 f"Umidade relativa: {humidity}%\n" \
                 f"Período: {is_day}"
        return result
    except requests.RequestException as e:
        return f"Erro ao obter previsão do tempo: {str(e)}"

# 3. Execute o servidor
if __name__ == "__main__":
    mcp.run()     

    #https://api.open-meteo.com/v1/forecast?latitude=-26.3044&longitude=-48.8456&current=temperature_2m,precipitation,rain,showers,is_day,apparent_temperature,relative_humidity_2m&forecast_days=1     