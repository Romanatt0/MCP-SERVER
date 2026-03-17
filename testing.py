import asyncio

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    llm = ChatOllama(model="gemma3:1b")

    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "Você é um assistente chamado Bot-Ville especializado na cidade de Joinville SC. "
        "Se precisar de dados de clima use a ferramenta de previsão."),
        ("human", "{input}")
    ])


    client = MultiServerMCPClient({
        "joinville": {
            "transport": "http",
            "url": "http://127.0.0.1:8000/mcp"
        }
    })

    tools = await client.get_tools()

    agent = create_agent(
		model=llm,
		tools=tools,
		system_prompt="Você é um assistente chamado Bot-Ville especializado na cidade de Joinville SC. Se precisar de dados de clima use a ferramenta de previsão."
	)

    while True:
        user_text = input("Você: ")
   
        response = await agent.ainvoke({"input": user_text})

		# response["output"] contém a resposta final do Bot-Ville
        print("Bot-Ville:", response["output"])

asyncio.run(main())