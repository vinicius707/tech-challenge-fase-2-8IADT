# Experiments — metodologia e padrões

Este documento descreve como configurar, executar e reportar experimentos reprodutíveis.

1) Organização de pastas

- `experiments/configs/` — arquivos YAML de configuração por experimento.  
- `experiments/run_<timestamp>/` — artefatos gerados por execução: `history.csv`, `best_solution.csv`, `routes.geojson`, `route_map.html`, `results.csv`, `instruction.txt`.
- `experiments/batch_runs/` — runs em lote e `aggregate_results.csv`.

2) Padrões para configuração

- Use YAML em `experiments/configs/` com chaves: `ga`, `vehicle`, `fitness_weights`, `experiment`.  
- Salve seeds/seed reproducible em `experiment.seed`.

3) Executando um experimento (manual)

```bash
PYTHONPATH=. python3 scripts/run_ga_example.py
PYTHONPATH=. python3 scripts/export_artifacts.py experiments/run_<timestamp>
PYTHONPATH=. python3 scripts/generate_instructions.py experiments/run_<timestamp>
```

4) Experimentos em batch

- Use `scripts/run_experiments.py` para rodar variações automatizadas e gerar `aggregate_results.csv`.
- Use `notebooks/compare_results.ipynb` para analisar e comparar resultados.

5) Relatórios e apresentações

- Para cada experimento inclua: configuração (YAML), `history.csv`, plots (convergência), `results.csv`, mapa (HTML) e `instruction.txt`.

