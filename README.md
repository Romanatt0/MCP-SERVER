# MCP-SERVER — Clima de Joinville

Servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io) em Python que fornece a um LLM/chatbot
informações do tempo em **Joinville - SC**, usando a API gratuita da [Open-Meteo](https://open-meteo.com)
(não precisa de chave de API).

Construído com [FastMCP](https://gofastmcp.com) e servido via HTTP.

## Ferramentas (tools)

| Nome | Parâmetros | Quando o modelo usa |
|------|------------|---------------------|
| `previsao_tempo_joinville` | — | Perguntas sobre o tempo **agora**: temperatura, sensação térmica, umidade, se está chovendo. |
| `previsao_proximos_dias_joinville` | `dias` (int, 1–16, padrão 7) | Perguntas sobre **amanhã, a semana, o fim de semana** ou uma data futura. |

Exemplo de retorno de `previsao_proximos_dias_joinville` com `dias=3`:

```
Previsão para Joinville - SC nos próximos 3 dia(s):
- domingo 15/11: pancadas de chuva fracas; mín 20.5°C, máx 28.8°C; chance de chuva 90%, volume 4.9 mm
- segunda 16/11: pancadas de chuva fracas; mín 20.4°C, máx 26.6°C; chance de chuva 86%, volume 7.8 mm
- terça 17/11: garoa moderada; mín 20.7°C, máx 27.9°C; chance de chuva 73%, volume 3.2 mm
```

As respostas da API são validadas com modelos Pydantic (`src/models/model.py`) antes de serem formatadas.

## Estrutura

```
src/
├── my_server.py       # servidor MCP e ferramentas
└── models/
    └── model.py       # modelos Pydantic das respostas da Open-Meteo
```

## Como rodar

Requer Python 3.10+.

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

cd src
python my_server.py
```

O servidor sobe em **`http://localhost:8000/mcp`** (transporte HTTP streamable).

> Rode a partir da pasta `src/`, pois o import `from models.model import ...` é relativo a ela.

## Como conectar

**Claude Code**

```bash
claude mcp add --transport http clima-joinville http://localhost:8000/mcp
```

**Cliente Python (FastMCP)** — útil para testar:

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        print([t.name for t in tools])

        result = await client.call_tool("previsao_proximos_dias_joinville", {"dias": 3})
        print(result.content[0].text)

asyncio.run(main())
```

Qualquer outro cliente MCP com suporte a HTTP (LangChain via `langchain-mcp-adapters`, Claude Desktop etc.)
pode se conectar pela mesma URL.
