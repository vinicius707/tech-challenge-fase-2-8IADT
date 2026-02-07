# Runtime — Como executar o GA e interpretar artefatos

Este documento descreve como rodar o loop do Algoritmo Genético e onde encontrar os artefatos gerados.

Comando de exemplo (usa configuração em `experiments/configs/experiment_01.yaml`):

```bash
PYTHONPATH=. python3 scripts/run_ga_example.py
```

O runner gera um diretório `experiments/run_<timestamp>/` contendo:

- `history.csv` — histórico por geração (generation, best_fitness, avg_fitness).  
- `best_solution.csv` — rotas do melhor indivíduo (route_index, sequence).  

Parâmetros disponíveis (no script de exemplo / YAML):
- num_vehicles, population, generations, elitism, mutation_rate, fitness_weights.

Interpretação rápida:
- Observe `history.csv` para verificar convergência da fitness (deve decrescer).  
- `best_solution.csv` traz a sequência de IDs por veículo — utilize `docs/implementation_notes.md` e `docs/output_formats.md` (quando disponível) para exportar geojson/html.

