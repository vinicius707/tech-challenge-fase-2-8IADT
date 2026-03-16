# Testing Guide

Este documento descreve como executar os testes do repositório, interpretar resultados e as convenções para adicionar novos testes.

1) Executar todos os testes (rápido)

```bash
PYTHONPATH=. pytest -q
```

2) Testes de API

- Os testes de API usam `fastapi.testclient` e executam o GA em background. Podem demorar alguns segundos.
- Executar apenas os testes de API:

```bash
PYTHONPATH=. pytest -q tests/api/test_api.py
```

3) Rodar testes específicos (ex.: fitness)

```bash
PYTHONPATH=. pytest -q tests/ga/test_fitness.py
```

4) Cobertura (opcional)

Instale `coverage` e rode:

```bash
pip install coverage
coverage run -m pytest
coverage report -m
```

5) Test data / fixtures

- Os testes usam `data/instances/hospital_points.csv` como instância de exemplo. Para criar fixtures, coloque arquivos em `tests/fixtures/` e referencie-os nos testes (`tmp_path` pytest fixture pode ser usado).

6) CI

- O workflow `.github/workflows/ci.yml` executa os testes em PRs e pushes para `main`. Caso adicione testes demorados (experiments), considere marcá-los com `@integration` e rodá-los em um workflow separado.

7) Como adicionar testes

- Escreva testes pequenos e determinísticos. Para funções estocásticas, use `random.seed(...)` ou mocks.  
- Nomeie testes com `test_<func>.py` e inclua no diretório `tests/`.

