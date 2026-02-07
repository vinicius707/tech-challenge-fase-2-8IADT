# Tech Challenge — Fase 2 (Foco: Projeto 2 — Otimização de Rotas Médicas)

Este repositório documenta a proposta e as orientações para implementar o Projeto 2: otimização de rotas para distribuição de medicamentos e insumos em contexto hospitalar, usando Algoritmos Genéticos (AG) e integração com LLMs para geração de instruções e relatórios.

> Fonte do enunciado: `8IADT - Fase 2 - Tech challenge (1).pdf`

## Visão geral

O objetivo é desenvolver um sistema de otimização de rotas (TSP/VRP) adaptado às restrições de um ambiente hospitalar: prioridades de entregas, capacidade dos veículos, autonomia, múltiplos veículos e janelas de tempo, quando aplicável. A solução deve oferecer visualização das rotas e geração de instruções/relatórios em linguagem natural via LLM.

## Objetivos específicos (Projeto 2)

- Implementar representação genética adequada para rotas (codificação de caminhos).  
- Projetar operadores genéticos especializados (seleção, crossover, mutação) para TSP/VRP.  
- Criar função fitness que considere distância, prioridade das entregas, capacidade de carga e autonomia dos veículos.  
- Incluir restrições realistas: prioridades, capacidades, autonomia, múltiplos veículos (VRP).  
- Visualizar rotas otimizadas em mapa (HTML/JS) e exportar resultados (CSV/GeoJSON).  
- Integrar LLM para gerar instruções detalhadas e relatórios de eficiência.  
- Realizar ao menos 3 experimentos variando parâmetros do AG e documentar comparativos.

## Requisitos técnicos (detalhado)

1. Partir do código-base de TSP fornecido e adaptá-lo para o contexto hospitalar.  
2. Implementar operadores genéticos apropriados para sequências de rota (e.g., order crossover, swap mutation).  
3. Definir e justificar a função fitness (peso entre distância, prioridade, capacidade, tempo).  
4. Adicionar logging/monitoramento para experimento (salvar histórico de fitness por geração).  
5. Gerar visualizações: mapa interativo (folium/kepler.gl) e gráfico de convergência.  
6. Implementar endpoints mínimos (se optar por API): otimização, status de job, recuperação de rotas.  
7. Documentar arquitetura, decisões, limitações e resultados no relatório técnico.

## Entregáveis (Projeto 2)

- Código-fonte modificado a partir do TSP base.  
- Notebooks/scripts de demonstração (ex.: executar experimento e gerar mapa).  
- Pasta `experiments/` com resultados (CSV), plots e HTMLs das rotas.  
- Relatório técnico (metodologia, configurações, métricas e comparativos).  
- Vídeo de demonstração (até 15 minutos) mostrando: execução, visualização de rotas e exemplo de instrução gerada pela LLM.

## Instalação e execução (exemplos focados em Projeto 2)

Recomenda-se Python 3.10+. Exemplos abaixo via venv e Poetry.

Usando venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# exemplo: rodar experimento de otimização
python -m src.optimize --config experiments/configs/experiment_01.yaml
```

Exemplo de `requirements.txt` mínimo (sugestão):

```text
numpy
pandas
networkx
folium
geopandas
shapely
matplotlib
pytest
requests
openai  # se usar OpenAI para LLM
```

Usando Poetry:

```bash
poetry install
poetry run python -m src.optimize --config experiments/configs/experiment_01.yaml
```

Exemplo simples (rodando o TSP base):

```bash
python src/tsp/run_tsp.py --input data/instances/hospital_points.csv --output experiments/run_001/
# gera arquivos: routes.geojson, results.csv, route_map.html
```

Com Docker (opcional):

```bash
docker build -t tech-challenge-routes:latest .
docker run --rm -v $(pwd)/experiments:/app/experiments tech-challenge-routes:latest \
  python -m src.optimize --config experiments/configs/experiment_01.yaml
```

## Estrutura sugerida do repositório (foco Projeto 2)

```
.
├─ README.md
├─ requirements.txt / pyproject.toml
├─ Dockerfile
├─ data/                   # instâncias, pontos de entrega, malhas viárias (opcional)
├─ notebooks/              # notebooks de experimento / demonstração
├─ src/
│  ├─ tsp/                 # código-base TSP fornecido (adaptado)
│  ├─ ga/                  # implementação do Algoritmo Genético para roteamento
│  ├─ viz/                 # geração de mapas (folium) e plots
│  ├─ api/                 # API (FastAPI/Flask) se aplicável
│  └─ optimize.py          # runner para experimentos
├─ experiments/
│  ├─ configs/             # arquivos de configuração dos experimentos (yaml)
│  ├─ run_001/             # resultados de um experimento (csv, plots, html)
├─ tests/
└─ docs/
```

## Tecnologias e bibliotecas recomendadas

- Python 3.10+  
- Algoritmos genéticos: implementação própria ou libs auxiliares (de preferência customizada para controle dos operadores).  
- Grafos/roteamento: `networkx`, `ortools` (opcional para baseline).  
- Geoprocessamento/visualização: `geopandas`, `shapely`, `folium`, `kepler.gl` (opcional).  
- Experimentos: `pandas`, `matplotlib`, `seaborn`.  
- LLMs: `openai` (ou integração com modelo local).  
- API (opcional): `FastAPI` + `uvicorn`.

## Endpoints sugeridos (API)

- POST /optimize
  - Inicia job de otimização. Parâmetros: instancia, população, mutação, geracoes, constraints.
  - Retorna: job_id.
- GET /jobs/{job_id}
  - Retorna status, métricas parciais e link para artefatos.
- GET /routes/{job_id}
  - Retorna geojson das rotas, CSV com ordenação de entregas e HTML do mapa.
- POST /instructions/{route_id}
  - Gera instruções detalhadas para motorista/equipe usando LLM.

## Métricas e experimentos

Avalie especialmente:
- Distância total percorrida.  
- Tempo estimado (se disponível).  
- Número de veículos utilizados.  
- Cumprimento de prioridades (penalidades aplicadas na fitness).  
- Carga utilizada vs capacidade.  

Organize resultados por experimento em `experiments/{run_id}/results.csv` e inclua `plots/convergence.png` e `route_map.html`.

## Visualização das rotas

- Gere mapas interativos (folium) e exporte como `route_map.html`.  
- Para análise, exporte `routes.geojson` com propriedades (vehicle_id, sequence, load, priority).

Exemplo rápido (folium):

```python
import folium
m = folium.Map(location=[-23.55, -46.63], zoom_start=12)
folium.PolyLine([(lat1, lon1), (lat2, lon2), ...]).add_to(m)
m.save('route_map.html')
```

## Testes e CI

- Escreva testes unitários para operadores genéticos, função fitness e parsers de instância.  
- Exemplo de comando:

```bash
pytest -q
```

- Sugestão de CI: GitHub Actions que execute lint (flake8/ruff), testes e workflow de experimentos (opcional).

## Deploy / Infraestrutura como Código (opcional)

- Se usar nuvem, documente: como executar jobs em batch, armazenamento de artefatos e endpoints.  
- Exemplos: containerizar runner e usar AWS Batch / ECS, ou deploy de API com Fargate.

## Licença

Por padrão: MIT License. Substitua se for necessário outra licença.

```
MIT License
```

## Como contribuir

- Abra issues detalhando bugs/funcionalidades.  
- Pull requests pequenos com testes e descrição.  
- Siga PEP8/PEP257; inclua testes para novas funções.

---

Se quiser, eu posso agora:
- gerar `requirements.txt` / `pyproject.toml` com versões recomendadas,  
- criar template de `Dockerfile`, `openapi.yaml` ou um workflow GitHub Actions para rodar testes/experimentos.