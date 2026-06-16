# Exercício 4.2 - MCP local para tarefas

Este repositório contém a solução do exercício 4.2 de Governo Digital. O objetivo é criar um servidor MCP local, executado via stdio, que expõe ferramentas para interagir com a API REST de tarefas construída no exercício 4.1.

O exercício depende da API do 4.1 rodando em:

```text
http://localhost:8000
```

O servidor MCP oferece duas tools:

- `criar_tarefa(titulo: str)`: cria uma tarefa usando `POST /tarefas`.
- `listar_tarefas()`: lista as tarefas usando `GET /tarefas`.

## Instalação

```bash
pip install -r requirements.txt
```

## Como rodar

Com a API do exercício 4.1 em execução, rode:

```bash
python cliente_teste.py
```

O cliente sobe `servidor_mcp.py` via stdio, lista as tools disponíveis, chama `criar_tarefa("tarefa via mcp")`, chama `listar_tarefas()` e imprime apenas um envelope JSON no stdout.

## Como validar

```bash
autograde validar 4.2
```
