import httpx
from mcp.server.fastmcp import FastMCP


API_BASE_URL = "http://localhost:8000"

mcp = FastMCP("tarefas-governo-digital")


@mcp.tool()
def criar_tarefa(titulo: str) -> dict:
    with httpx.Client(base_url=API_BASE_URL, timeout=10.0) as client:
        response = client.post("/tarefas", json={"titulo": titulo})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def listar_tarefas() -> list:
    with httpx.Client(base_url=API_BASE_URL, timeout=10.0) as client:
        response = client.get("/tarefas")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
