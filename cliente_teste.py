import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def extrair_json(resultado: Any, *, como_lista: bool = False) -> Any:
    structured = getattr(resultado, "structured_content", None)
    if structured is None:
        structured = getattr(resultado, "structuredContent", None)
    if structured is not None:
        if isinstance(structured, dict) and set(structured) == {"result"}:
            structured = structured["result"]
        if como_lista and not isinstance(structured, list):
            return [structured]
        return structured

    if not resultado.content:
        return [] if como_lista else None

    payloads = []
    for item in resultado.content:
        texto = getattr(item, "text", "")
        payload = json.loads(texto)
        if isinstance(payload, dict) and set(payload) == {"result"}:
            payload = payload["result"]
        if isinstance(payload, list):
            payloads.extend(payload)
        else:
            payloads.append(payload)

    if como_lista:
        return payloads
    return payloads[0]


def normalizar_tarefa(tarefa: dict) -> dict:
    return {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "concluida": tarefa["concluida"],
    }


async def main() -> None:
    servidor = Path(__file__).with_name("servidor_mcp.py")
    parametros = StdioServerParameters(
        command=sys.executable,
        args=[str(servidor)],
    )

    with open(os.devnull, "w", encoding="utf-8") as errlog:
        async with stdio_client(parametros, errlog=errlog) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools_resultado = await session.list_tools()
                tools_disponiveis = [tool.name for tool in tools_resultado.tools]
                tools = [
                    nome
                    for nome in ["criar_tarefa", "listar_tarefas"]
                    if nome in tools_disponiveis
                ]

                criar = await session.call_tool(
                    "criar_tarefa",
                    {"titulo": "tarefa via mcp"},
                )
                listar = await session.call_tool("listar_tarefas", {})

    criar_payload = normalizar_tarefa(extrair_json(criar))
    listar_payload = [
        normalizar_tarefa(tarefa) for tarefa in extrair_json(listar, como_lista=True)
    ]

    envelope = {
        "tools": tools,
        "criar_resultado": criar_payload,
        "listar_resultado": listar_payload,
    }
    print(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    asyncio.run(main())
