# Output formats

Este documento descreve os artefatos gerados pelo runner e pelo export script.

1) history.csv
- Local: experiments/run_<timestamp>/history.csv
- Colunas: generation, best_fitness, avg_fitness

2) best_solution.csv
- Local: experiments/run_<timestamp>/best_solution.csv
- Colunas: route_index, sequence (IDs separados por '|')

3) routes.geojson
- GeoJSON FeatureCollection com uma Feature por veículo (LineString)
- Propriedades por feature: vehicle_id, sequence (array de IDs), load, priorities

4) route_map.html
- Mapa interativo (folium) com polylines por veículo e marcadores dos pontos

5) results.csv
- Colunas: total_distance, total_load, vehicles
- Gerado pelo script `scripts/export_artifacts.py`.
