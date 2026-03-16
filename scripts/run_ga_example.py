#!/usr/bin/env python3
import yaml
from src.ga import representation, engine
import os

CFG_PATH = "experiments/configs/experiment_01.yaml"

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return yaml.safe_load(fh)
    except Exception:
        return {}

def main():
    cfg = load_config(CFG_PATH)
    points = representation.parse_instance_csv(cfg.get("instance", "data/instances/hospital_points.csv"))
    num_vehicles = cfg.get("vehicle", {}).get("num_vehicles", 3)
    pop = cfg.get("ga", {}).get("population", 30)
    gens = cfg.get("ga", {}).get("generations", 10)
    elitism = cfg.get("ga", {}).get("elitism", 1)
    mutation_rate = cfg.get("ga", {}).get("mutation_rate", 0.05)
    weights = cfg.get("fitness_weights", {"distance": 1.0, "capacity_penalty": 1.0, "priority_penalty": 1.0, "vehicle_capacity": 100.0})

    out = engine.run_ga(points, num_vehicles=num_vehicles, population_size=pop, generations=gens, elitism=elitism, mutation_rate=mutation_rate, weights=weights)
    print("GA finished. Artifacts:", out)

if __name__ == "__main__":
    main()

