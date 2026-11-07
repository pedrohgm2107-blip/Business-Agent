import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ferramentas import listar_documentos, listar_incompletos, abrir_chamado, resumo

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = "gemini-3.5-flash-lite"

INSTRUCAO = """Voce e um assistente de RH.
Use as ferramentas para consultar documentos e abrir chamados.
Nunca invente dados: se a informacao nao vier de uma ferramenta, diga que nao sabe.
Depois de executar acoes, conte ao usuario exatamente o que foi feito."""


def criar_chat():
    config = types.GenerateContentConfig(
        system_instruction=INSTRUCAO,
        tools=[listar_documentos, listar_incompletos, abrir_chamado, resumo],
    )
    return client.chats.create(model=MODELO, config=config)


if __name__ == "__main__":
    chat = criar_chat()
    print("Agente de RH. Digite 'sair' para encerrar.")
    while True:
        pergunta = input("\nVoce: ")
        if pergunta.strip().lower() == "sair":
            break
        resposta = chat.send_message(pergunta)
        print("\nAgente:", resposta.text or "(sem resposta, tente reformular a pergunta)")