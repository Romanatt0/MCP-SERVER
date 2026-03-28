from fastmcp import FastMCP
import requests
from models.model import Forecast

mcp = FastMCP("MeuServidorMCP")     
print(f"Servidor MCP '{mcp.name}' inicializado.")

@mcp.tool(
        name="previsao_tempo_joinville",
        description="Retorna a previsão do tempo atual para uma cidade. Use esta ferramenta sempre que o usuário perguntar sobre clima, temperatura, chuva ou tempo em Joinville SC."
)
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
        data: Forecast = response.json()
        
  
        return str(data)
    except requests.RequestException as e:
        return f"Erro ao obter previsão do tempo: {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
    