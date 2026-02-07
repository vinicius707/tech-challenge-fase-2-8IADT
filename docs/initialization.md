# Inicialização — Heurísticas disponíveis

Este documento descreve as heurísticas de inicialização disponíveis para gerar a população inicial.

1) nearest_neighbor_init\n
- Implementação: `src/ga/initialization.py::nearest_neighbor_init`\n
- Estratégia: escolhe seeds e cresce cada rota adicionando o ponto não visitado mais próximo.\n
2) clarke_wright_savings\n
- Implementação: `src/ga/initialization.py::clarke_wright_savings`\n
- Estratégia: calcula savings entre pares e faz merges greedily até chegar ao número de veículos.\n
\n+Uso e validação\n\nExecute os testes: `PYTHONPATH=. pytest -q tests/ga/test_initialization.py`.\n
