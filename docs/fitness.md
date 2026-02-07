# Fitness — métricas e penalidades

Este documento descreve a função de fitness inicial usada para avaliar soluções VRP.

1) Fórmula básica

Fitness (quanto menor, melhor) é calculado como:

```
fitness = w_distance * total_distance + w_capacity * capacity_penalty + w_priority * priority_penalty
```

- total_distance: soma das distâncias de todas as rotas (em km), calculada via Haversine.  
- capacity_penalty: penalidade quando a soma dos volumes em uma rota excede a capacidade do veículo (ex.: soma(max(0, load - capacity)) ).  
- priority_penalty: penalidade se entregas de alta prioridade não forem atendidas ou forem demasiadamente atrasadas (definição a refinar).

2) Pesos configuráveis

Os pesos são lidos do arquivo de configuração YAML (`experiments/configs/*.yaml`) e permitem balancear distância vs. restrições.

3) Notas de implementação

- Usamos Haversine para calcular distância entre coordenadas (lat/lon).  
- Penalidades são multiplicadas por fatores configuráveis; inicialmente são placeholders mas implementarão fórmulas lineares ou escalonadas.

5) Fórmulas de penalidade (implementação atual)

- capacity_penalty = sum_over_routes(max(0, load_route - vehicle_capacity))
- priority_penalty = sum_over_routes(sum(index_of_stop for each high-priority stop))

Exemplo de configuração YAML:

```yaml
fitness_weights:
  distance: 0.6
  capacity_penalty: 1.0
  priority_penalty: 2.0
vehicle:
  capacity: 100.0
```

6) Testes

Testes unitários em `tests/ga/test_fitness.py` validam Haversine, total_distance_for_route e fitness quando apenas distância é considerada.

