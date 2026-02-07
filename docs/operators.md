# Operadores Genéticos — Implementação e uso

Este documento descreve os operadores genéticos básicos implementados para o Projeto 2.

Operadores disponíveis (implementados em `src/ga/operators.py`)

- relocate(chromosome): move um cliente aleatório de uma rota para outra. Mantém cobertura e não duplica pontos. Útil para exploração entre rotas.
- swap(chromosome): troca dois clientes (entre rotas ou intra-rota). Mantém cobertura completa.
- two_opt(route): aplica 2-opt em uma única rota (inverte um segmento) para melhoria local.
 - crossover_vrp(parent1, parent2, num_vehicles): aplica Order Crossover (OX) em sequências achatadas e redistribui a sequência resultante entre veículos (split round-robin). Útil como operador de recombinação entre soluções.

Exemplo de uso:

```python
from src.ga import operators

chrom = [[1,2,3],[4,5],[6]]
chrom2 = operators.relocate(chrom)
chrom3 = operators.swap(chrom2)
chrom3[0] = operators.two_opt(chrom3[0])
```

Notas:
- Os operadores atuais são estocásticos (aleatórios). Em produção, combine operadores com probabilidades parametrizáveis no GA.
- Testes básicos estão em `tests/ga/test_operators.py`.

