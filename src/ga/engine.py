from typing import List, Dict, Any, Optional, Callable
import os
import time
import csv
import random

from . import representation, population, operators, fitness
from . import initialization


def _compute_depot(points: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not points:
        return {"lat": 0.0, "lon": 0.0}
    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]
    return {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}


def run_ga(points: List[Dict[str, Any]],
           num_vehicles: int = 3,
           population_size: int = 30,
           generations: int = 50,
           elitism: int = 1,
           mutation_rate: float = 0.1,
           selection_method: str = "tournament",
           weights: Dict[str, float] = None,
           depot: Dict[str, Any] = None,
           init_method: str = "random",
           out_dir: str = None,
           on_progress: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
    """
    Simple GA runner.
    Saves history.csv and best_solution.csv in out_dir.
    init_method: "random" (default), "nearest_neighbor", or "clarke_wright" — seeds population with heuristic.
    depot: if None, computed as centroid of points. Used for fitness and heuristic initialization.
    Returns dict with paths.
    """
    if weights is None:
        weights = {"distance": 1.0, "capacity_penalty": 1.0, "priority_penalty": 1.0, "vehicle_capacity": 100.0}

    if out_dir is None:
        out_dir = f"experiments/run_{int(time.time())}"
    os.makedirs(out_dir, exist_ok=True)

    depot = depot or _compute_depot(points)
    ids = [p["id"] for p in points]
    lookup = representation.build_points_lookup(points)

    # init population
    pop = population.generate_random_population(ids, num_vehicles, population_size)
    if init_method == "nearest_neighbor":
        seed = initialization.nearest_neighbor_init(points, num_vehicles, depot=depot)
        if pop:
            pop[0] = seed
    elif init_method == "clarke_wright":
        seed = initialization.clarke_wright_savings(points, num_vehicles, depot=depot)
        if pop:
            pop[0] = seed

    history = []
    best_solution = None
    best_fitness = float("inf")

    for gen in range(generations):
        fitnesses = []
        for chrom in pop:
            decoded = representation.decode_chromosome(chrom, lookup)
            f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
            fitnesses.append(f)

        avg_f = sum(fitnesses) / len(fitnesses)
        sorted_idx = sorted(range(len(pop)), key=lambda i: fitnesses[i])
        gen_best = fitnesses[sorted_idx[0]]
        history.append({"generation": gen, "best_fitness": gen_best, "avg_fitness": avg_f})

        if gen_best < best_fitness:
            best_fitness = gen_best
            best_solution = pop[sorted_idx[0]]

        # create next generation
        new_pop = []
        # elitism
        for i in range(elitism):
            new_pop.append(pop[sorted_idx[i]])

        while len(new_pop) < population_size:
            # selection
            if selection_method == "tournament":
                parent1 = population.tournament_selection(pop, fitnesses, k=3)
                parent2 = population.tournament_selection(pop, fitnesses, k=3)
            else:
                parent1 = population.roulette_selection(pop, fitnesses)
                parent2 = population.roulette_selection(pop, fitnesses)

            # crossover
            child = operators.crossover_vrp(parent1, parent2, num_vehicles)

            # mutation
            if random.random() < mutation_rate:
                child = operators.relocate(child)
            if random.random() < mutation_rate:
                child = operators.swap(child)
            # apply 2-opt per route with small chance
            for ri in range(len(child)):
                if random.random() < (mutation_rate / 2):
                    child[ri] = operators.two_opt(child[ri])

            new_pop.append(child)

        pop = new_pop

        if on_progress:
            on_progress(gen + 1, generations)

        # checkpoint: save history each generation
        hist_path = os.path.join(out_dir, "history.csv")
        with open(hist_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["generation", "best_fitness", "avg_fitness"])
            writer.writeheader()
            for row in history:
                writer.writerow(row)

    # save best solution
    best_path = os.path.join(out_dir, "best_solution.csv")
    with open(best_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["route_index", "sequence"])
        for i, route in enumerate(best_solution):
            writer.writerow([i, "|".join(str(x) for x in route)])

    return {"out_dir": out_dir, "history": hist_path, "best": best_path}

