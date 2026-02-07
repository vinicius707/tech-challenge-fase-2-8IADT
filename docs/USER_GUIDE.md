# User Guide — Tech Challenge (Projeto 2) Quickstart e Guia Completo

Este guia foi criado para tornar a documentação acessível a todos os níveis: iniciantes, usuários que querem rodar exemplos, e desenvolvedores que vão estender o código.

1) Objetivo rápido

- Executar um experimento de otimização de rotas (GA), exportar artefatos (geojson, mapa HTML, results.csv) e gerar instruções em linguagem natural via LLM.

2) Requisitos básicos

- Python 3.10+, `pip` ou `poetry`.  
- (Recomendado) Instalar dependências do sistema para geospatial — veja `scripts/install_system_deps.sh` ou README.md.

3) Quickstart — passos mínimos (5 minutos)

- Criar e ativar venv:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- Rodar validações iniciais:
  ```bash
  PYTHONPATH=. python3 scripts/validate_parse.py
  PYTHONPATH=. python3 scripts/validate_repr.py
  ```
- Rodar GA de exemplo (curto):
  ```bash
  PYTHONPATH=. python3 scripts/run_ga_example.py
  ```
- Exportar artefatos do run gerado (substitua <timestamp>):
  ```bash
  PYTHONPATH=. python3 scripts/export_artifacts.py experiments/run_<timestamp>
  ```
- Gerar instruções (fallback se sem OPENAI_API_KEY):
  ```bash
  PYTHONPATH=. python3 scripts/generate_instructions.py experiments/run_<timestamp>
  ```

4) Seções para iniciantes

- Se preferir GUI: abra `experiments/run_<timestamp>/route_map.html` no navegador para ver rotas.  
- `experiments/run_<timestamp>/instruction.txt` contém instruções passo-a-passo (geradas pelo LLM ou fallback).

5) Para desenvolvedores — mapa rápido dos módulos

- `src/ga/representation.py` — parser CSV, encode/decode chromosome.  
- `src/ga/fitness.py` — Haversine + penalidades (capacidade, prioridade).  
- `src/ga/operators.py` — relocate, swap, 2-opt, crossover_vrp.  
- `src/ga/initialization.py` — heurísticas: nearest neighbor, Clarke-Wright.  
- `src/ga/population.py` — geração de população, tournament/roulette selection.  
- `src/ga/engine.py` — loop GA (elitism, mutation, checkpointing).  
- `src/viz/map.py` — geração de GeoJSON e mapa HTML (folium).  
- `src/llm/adapter.py` — adapter OpenAI + fallback.  
- `src/api/app.py` — FastAPI endpoints para submeter jobs e recuperar artefatos.

6) Testes

- Rodar todos os testes:
  ```bash
  PYTHONPATH=. pytest -q
  ```
- Testes de API usam TestClient (executam o GA em background, podem demorar alguns segundos).

7) Troubleshooting comum

- Erro `ModuleNotFoundError: No module named 'fastapi'` — instale deps (`pip install -r requirements.txt`).  
- Erro ao instalar pacotes geoespaciais — prefira `conda` ou crie wheelhouse via `scripts/build_wheelhouse.sh`.
- Docker: verifique Docker Desktop rodando no macOS/Windows.

8) Contribuição e fluxo

- Branches: `feat/vrp-<short>`; commits: `type(scope): short description`.  
- Fluxo por etapa: Implement → Test → Commit → Docs → PR.

9) Links úteis (docs internos)

- README.md — visão geral e quickstart  
- docs/design_repr.md — representação VRP  
- docs/fitness.md — métricas e penalidades  
- docs/operators.md — operadores genéticos  
- docs/initialization.md — heurísticas de inicialização  
- docs/runtime.md — execução do runner e interpretação de artefatos  
- docs/output_formats.md — formatos de saída  
- docs/llm_integration.md — integração com LLMs  
- docs/api.md — API endpoints e uso

---

Se quiser, eu posso também gerar tutoriais rápidos em notebooks (`notebooks/`) mostrando passo-a-passo com outputs e screenshots (recomendado para apresentação).

