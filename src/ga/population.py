from typing import List, Dict, Any
import random

def generate_random_population(points_ids: List[int], num_vehicles: int, population_size: int) -> List[List[List[int]]]:
    """
    Generate a population of chromosomes. Each chromosome is a list of routes (list of int IDs).
    """
    population = []
    for _ in range(population_size):
        perm = points_ids[:]
        random.shuffle(perm)
        # naive split
        chrom = [[] for _ in range(num_vehicles)]
        for idx, pid in enumerate(perm):
            chrom[idx % num_vehicles].append(pid)
        population.append(chrom)
    return population

def tournament_selection(population: List[List[List[int]]], fitnesses: List[float], k: int=3) -> List[List[int]]:
    """
    Select one individual using tournament selection.
    """
    participants = random.sample(range(len(population)), k)
    participants = sorted(participants, key=lambda i: fitnesses[i])
    return population[participants[0]]


def roulette_selection(population: List[List[List[int]]], fitnesses: List[float]) -> List[List[int]]:
    """
    Roulette wheel selection (fitness must be positive; lower fitness = better so we invert).
    """
    # convert to positive scores where higher is better
    max_f = max(fitnesses) if fitnesses else 0.0
    scores = [max_f - f + 1e-6 for f in fitnesses]  # add epsilon
    total = sum(scores)
    if total <= 0:
        return random.choice(population)
    pick = random.uniform(0, total)
    current = 0.0
    for ind, s in enumerate(scores):
        current += s
        if current >= pick:
            return population[ind]
    return population[-1]

