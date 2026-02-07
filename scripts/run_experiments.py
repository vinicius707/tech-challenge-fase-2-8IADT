#!/usr/bin/env python3
"""
Run a batch of experiments with varying GA parameters and aggregate results.
Generates experiments/aggregate_results.csv and simple JSON summary per run.
"""
import os
import csv
import time
from src.ga import engine, representation

RUN_DIR = "experiments/batch_runs"
os.makedirs(RUN_DIR, exist_ok=True)

# Define experiments (small for quick runs)
EXPERIMENTS = [
    {"name": "exp_pop50_gen20", "population": 50, "generations": 20, "mutation_rate": 0.05},
    {"name": "exp_pop80_gen20", "population": 80, "generations": 20, "mutation_rate": 0.05},
    {"name": "exp_pop50_gen40", "population": 50, "generations": 40, "mutation_rate": 0.02},
]

INSTANCE = "data/instances/hospital_points.csv"

AGG_PATH = os.path.join(RUN_DIR, "aggregate_results.csv")
with open(AGG_PATH, "w", newline="", encoding="utf-8") as agg_fh:
    writer = csv.writer(agg_fh)
    writer.writerow(["run_id", "name", "population", "generations", "mutation_rate", "best_fitness", "history_path", "best_path"])

    for cfg in EXPERIMENTS:
        run_id = int(time.time())
        out_dir = os.path.join(RUN_DIR, f"{cfg['name']}_{run_id}")
        os.makedirs(out_dir, exist_ok=True)
        points = representation.parse_instance_csv(INSTANCE)
        weights = {"distance": 1.0, "capacity_penalty": 1.0, "priority_penalty": 2.0, "vehicle_capacity": 100.0}
        res = engine.run_ga(points,
                            num_vehicles=3,
                            population_size=cfg["population"],
                            generations=cfg["generations"],
                            elitism=1,
                            mutation_rate=cfg["mutation_rate"],
                            weights=weights,
                            out_dir=out_dir)

        # read final best fitness from history
        history_path = res.get("history")
        best_fitness = None
        if history_path and os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as fh:
                lines = fh.read().strip().splitlines()
                if len(lines) > 1:
                    last = lines[-1].split(",")
                    best_fitness = float(last[1])

        writer.writerow([run_id, cfg["name"], cfg["population"], cfg["generations"], cfg["mutation_rate"], best_fitness, history_path, res.get("best")])
        print("Completed run:", cfg["name"], "out:", out_dir)

print("Aggregate results written to", AGG_PATH)

