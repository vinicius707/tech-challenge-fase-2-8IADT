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

