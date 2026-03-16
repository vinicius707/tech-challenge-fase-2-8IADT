# API — Endpoints mínimos

Implementação mínima de API para submeter jobs de otimização, consultar status e recuperar artefatos.

Aplicação: `src/api/app.py` (FastAPI)

Endpoints:

- POST /optimize
  - Inicia job de otimização (aceita payload JSON com `instance`, `num_vehicles`, `population`, `generations`, `mutation_rate`, `elitism`, `fitness_weights`).
  - Retorna: { job_id, status } (202).

- GET /jobs/{job_id}
  - Consulta status do job (queued, running, finished, failed) e metadados.

- GET /routes/{job_id}
  - Se job finalizado, retorna caminhos para artifacts (history.csv, best_solution.csv, etc).

- POST /instructions/{job_id}
  - Gera `instruction.txt` a partir de `routes.geojson` do job (usa LLMAdapter — OpenAI se disponível, fallback caso não).

Como executar localmente:

```bash
uvicorn src.api.app:app --reload --port 8000
```

