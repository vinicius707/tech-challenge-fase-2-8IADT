# Design da representação (VRP)

Este documento descreve a representação cromossômica inicial usada para o Projeto 2 (Otimização de Rotas Médicas).

Formato escolhido (inicial)

- Cromossoma: lista de rotas, onde cada rota é uma lista ordenada de IDs de pontos.
- Exemplo:

```python
[[1,4,7], [2,3,6,5], [8,9,10]]
```

Interpretação

- Cada sublista representa a sequência de entregas para um veículo.
- A solução deve cobrir todos os pontos exatamente uma vez (sem duplicações ou omissões).

Vantagens

- Representação direta e fácil de entender.
- Facilita aplicação de operadores específicos por rota (2-opt, intra-route swap) e operadores entre rotas (relocate, route-exchange).

Evolução futura

- Substituir encoder round-robin por heurísticas (savings, nearest neighbor) para inicialização.
- Suportar divisores em um cromossoma linear (lista com marcadores) se necessário.

## Para iniciantes (exemplo rápido)

- Passo 1: prepare o CSV de instância `data/instances/hospital_points.csv` com colunas `id,lat,lon,priority,volume,notes`.  
- Passo 2: execute o parser e veja o cromossoma inicial:

```bash
PYTHONPATH=. python3 - <<'PY'
from src.ga.representation import parse_instance_csv, build_points_lookup, encode_chromosome, decode_chromosome
pts = parse_instance_csv("data/instances/hospital_points.csv")
lookup = build_points_lookup(pts)
chrom = encode_chromosome(pts, num_vehicles=3)
print(decode_chromosome(chrom, lookup))
PY
```

## Para desenvolvedores

- Mantenha operações internas usando IDs (inteiros) e só faça lookup para export/visualização.  
- Crie testes que verifiquem que `encode` → `decode` cobre todos os IDs exatamente uma vez.

