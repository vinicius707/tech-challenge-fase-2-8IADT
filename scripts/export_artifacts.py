#!/usr/bin/env python3
import os
import csv
import json
import sys
from src.ga import representation
from src.viz import map as viz_map

def load_best_solution(path):
    routes = []
    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            seq = [int(x) for x in row['sequence'].split('|') if x]
            routes.append(seq)
    return routes

def compute_metrics(decoded_routes):
    total_distance = 0.0
    total_load = 0.0
    for route in decoded_routes:
        for p in route:
            total_load += p.get('volume', 0.0)
    return {"total_distance": total_distance, "total_load": total_load, "vehicles": len(decoded_routes)}

def main(out_dir: str):
    instance = "data/instances/hospital_points.csv"
    best_csv = os.path.join(out_dir, "best_solution.csv")
    if not os.path.exists(best_csv):
        print("best_solution.csv not found in", out_dir)
        sys.exit(1)

    points = representation.parse_instance_csv(instance)
    lookup = representation.build_points_lookup(points)
    routes = load_best_solution(best_csv)
    decoded = representation.decode_chromosome(routes, lookup)

    # geojson
    geojson_obj = viz_map.routes_to_geojson(decoded)
    geojson_path = os.path.join(out_dir, "routes.geojson")
    viz_map.save_geojson(geojson_obj, geojson_path)

    # map html
    html_path = os.path.join(out_dir, "route_map.html")
    viz_map.generate_simple_html_map(decoded, html_path)

    # results.csv (simple metrics)
    metrics = compute_metrics(decoded)
    results_path = os.path.join(out_dir, "results.csv")
    with open(results_path, "w", newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(["total_distance", "total_load", "vehicles"])
        writer.writerow([metrics["total_distance"], metrics["total_load"], metrics["vehicles"]])

    print("Exported artifacts to", out_dir)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print("Usage: export_artifacts.py <out_dir>")
