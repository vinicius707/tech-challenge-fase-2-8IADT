from typing import List, Dict, Any
import random
import copy

def relocate(chromosome: List[List[int]]) -> List[List[int]]:
    """
    Move a random customer from one route to another (simple relocate).
    """
    if not chromosome or len(chromosome) < 2:
        return chromosome
    new_chrom = copy.deepcopy(chromosome)
    # pick non-empty source route
    src = random.choice([i for i, r in enumerate(new_chrom) if r])
    dst = random.choice([i for i in range(len(new_chrom)) if i != src])
    idx = random.randrange(len(new_chrom[src]))
    customer = new_chrom[src].pop(idx)
    insert_pos = random.randrange(len(new_chrom[dst]) + 1)
    new_chrom[dst].insert(insert_pos, customer)
    return new_chrom


def swap(chromosome: List[List[int]]) -> List[List[int]]:
    """
    Swap two customers between routes (or within the same route).
    """
    if not chromosome:
        return chromosome
    new_chrom = copy.deepcopy(chromosome)
    routes_with_customers = [i for i, r in enumerate(new_chrom) if r]
    if len(routes_with_customers) < 1:
        return new_chrom
    r1 = random.choice(routes_with_customers)
    r2 = random.choice(routes_with_customers)
    i1 = random.randrange(len(new_chrom[r1]))
    i2 = random.randrange(len(new_chrom[r2]))
    new_chrom[r1][i1], new_chrom[r2][i2] = new_chrom[r2][i2], new_chrom[r1][i1]
    return new_chrom


def two_opt(route: List[int]) -> List[int]:
    """
    Simple 2-opt on a single route: pick two indices and reverse the segment.
    """
    if len(route) < 4:
        return route
    i = random.randint(0, len(route)-2)
    j = random.randint(i+1, len(route)-1)
    new_route = route[:i] + list(reversed(route[i:j+1])) + route[j+1:]
    return new_route

