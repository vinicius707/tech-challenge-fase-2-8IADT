#!/usr/bin/env python3
"""
Compara desempenho do Algoritmo Genético vs baseline greedy (nearest-neighbor).
Gera experiments/comparative_results.csv para o relatório técnico.
"""
import csv
import os
import sys
import time
import yaml

from src.ga import representation, engine, fitness
from src.baselines.greedy import run_nearest_neighbor


def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return {}


def _compute_depot(points: list) -> dict:
    if not points:
        return {"lat": 0.0, "lon": 0.0}
    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]
    return {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}


def eval_ga_result(best_csv: str, points: list, weights: dict, depot: dict) -> tuple:
    """Carrega best_solution.csv e retorna (fitness, total_distance_km, vehicles_used)."""
    if not best_csv or not os.path.exists(best_csv):
        return float("inf"), 0.0, 0
    lookup = representation.build_points_lookup(points)
    routes = []
    with open(best_csv, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            seq = [int(x) for x in row.get("sequence", "").split("|") if x]
            routes.append(seq)
    decoded = representation.decode_chromosome(routes, lookup)
    f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
    total_km = sum(fitness.total_distance_for_route(r, depot=depot) for r in decoded)
    return f, round(total_km, 2), len(decoded)


def main():
    cfg_path = os.environ.get("COMPARATIVE_CONFIG", "experiments/configs/experiment_01.yaml")
    instance = os.environ.get("INSTANCE", "data/instances/hospital_points.csv")

    cfg = load_config(cfg_path)
    instance = cfg.get("instance", instance)
    if not os.path.exists(instance):
        print(f"Instance not found: {instance}", file=sys.stderr)
        sys.exit(1)

    points = representation.parse_instance_csv(instance)
    num_vehicles = cfg.get("vehicle", {}).get("num_vehicles", 3)
    weights = cfg.get("fitness_weights", {
        "distance": 1.0,
        "capacity_penalty": 1.0,
        "priority_penalty": 1.0,
        "vehicle_capacity": 100.0,
    })
    depot = _compute_depot(points)

    ga_cfg = cfg.get("ga", {})
    pop = ga_cfg.get("population", 50)
    gens = ga_cfg.get("generations", 100)
    elitism = ga_cfg.get("elitism", 1)
    mutation_rate = ga_cfg.get("mutation_rate", 0.05)

    out_dir = "experiments/comparative_run"
    os.makedirs(out_dir, exist_ok=True)

    # Run GA
    t0 = time.perf_counter()
    ga_result = engine.run_ga(
        points,
        num_vehicles=num_vehicles,
        population_size=pop,
        generations=gens,
        elitism=elitism,
        mutation_rate=mutation_rate,
        weights=weights,
        depot=depot,
        out_dir=os.path.join(out_dir, "ga"),
    )
    ga_time = time.perf_counter() - t0

    ga_fitness, ga_km, ga_vehicles = eval_ga_result(
        ga_result.get("best"), points, weights, depot
    )

    # Run greedy
    t0 = time.perf_counter()
    greedy_result = run_nearest_neighbor(points, num_vehicles, weights, depot)
    greedy_time = time.perf_counter() - t0

    rows = [
        {
            "method": "ga",
            "instance": instance,
            "fitness": ga_fitness,
            "total_distance_km": ga_km,
            "vehicles_used": ga_vehicles,
            "runtime_sec": round(ga_time, 2),
        },
        {
            "method": "greedy_nearest_neighbor",
            "instance": instance,
            "fitness": greedy_result["fitness"],
            "total_distance_km": greedy_result["total_distance_km"],
            "vehicles_used": num_vehicles,
            "runtime_sec": round(greedy_time, 2),
        },
    ]

    results_path = "experiments/comparative_results.csv"
    os.makedirs("experiments", exist_ok=True)
    with open(results_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["method", "instance", "fitness", "total_distance_km", "vehicles_used", "runtime_sec"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resultados salvos em {results_path}")
    print("GA:    fitness={}, total_km={}, vehicles={}, time={:.2f}s".format(
        ga_fitness, ga_km, ga_vehicles, ga_time))
    print("Greedy: fitness={}, total_km={}, vehicles={}, time={:.2f}s".format(
        greedy_result["fitness"], greedy_result["total_distance_km"], num_vehicles, greedy_time))


if __name__ == "__main__":
    main()
