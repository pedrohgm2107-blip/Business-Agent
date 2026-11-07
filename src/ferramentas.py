import json
import os
from datetime import datetime
from openpyxl import load_workbook

PLANILHA = os.path.join("dados", "resultado.xlsx")
CHAMADOS = os.path.join("dados", "chamados.json")


def _ler_planilha():
    ws = load_workbook(PLANILHA).active
    linhas = list(ws.iter_rows(values_only=True))
    cabecalho = linhas[0]
    return [dict(zip(cabecalho, linha)) for linha in linhas[1:]]


def listar_documentos() -> list:
    """Lista todos os documentos com arquivo, nome do colaborador e status (OK ou INCOMPLETO)."""
    return [
        {"arquivo": d["arquivo"], "nome": d["nome"], "status": d["status"]}
        for d in _ler_planilha()
    ]


def listar_incompletos() -> list:
    """Lista apenas os documentos incompletos e quais campos estao faltando."""
    return [
        {"arquivo": d["arquivo"], "nome": d["nome"],
         "campos_faltando": d["campos_faltando"]}
        for d in _ler_planilha()
        if d["status"] == "INCOMPLETO"
    ]


def abrir_chamado(colaborador: str, assunto: str) -> dict:
    """Abre um chamado registrando o nome do colaborador e o assunto do pedido."""
    chamados = []
    if os.path.exists(CHAMADOS):
        with open(CHAMADOS, encoding="utf-8") as f:
            chamados = json.load(f)

    chamado = {
        "id": len(chamados) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "colaborador": colaborador,
        "assunto": assunto,
        "status": "aberto",
    }
    chamados.append(chamado)

    with open(CHAMADOS, "w", encoding="utf-8") as f:
        json.dump(chamados, f, ensure_ascii=False, indent=2)
    return chamado


if __name__ == "__main__":
    for item in listar_incompletos():
        print(item)