# API lib

`lib/api.js` — wrappers para a API FastAPI backend. A base URL é definida por `NEXT_PUBLIC_API_URL` (padrão: `http://localhost:8000`).

## Funções

### postOptimize(params)

Cria um novo job de otimização. Parâmetros: `instance`, `num_vehicles`, `population`, `generations`, `mutation_rate`, `elitism`.

Retorna: `{ job_id, status }`

### getJobs()

Lista todos os jobs. Retorna: `{ jobs: { [id]: { status, job_id } } }`

### getJob(jobId)

Obtém detalhes de um job. Retorna: objeto com `status`, `request`, `artifacts`, etc.

### getRoutes(jobId)

Obtém rotas/artifacts de um job concluído. Retorna: `{ status, artifacts }`

### postInstructions(jobId)

Gera instruções via LLM para um job concluído. Retorna: `{ status, instruction }` (path do arquivo).
