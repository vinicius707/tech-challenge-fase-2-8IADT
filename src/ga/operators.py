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


def flatten_chromosome(chromosome: List[List[int]]) -> List[int]:
    """Flatten list of routes into a single sequence preserving intra-route order."""
    return [cid for route in chromosome for cid in route]


def order_crossover_ids(parent1_seq: List[int], parent2_seq: List[int]) -> List[int]:
    """Order Crossover (OX) for sequences of IDs."""
    length = len(parent1_seq)
    if length == 0:
        return []
    a = random.randint(0, length - 2)
    b = random.randint(a + 1, length - 1)
    child = [None] * length
    # copy slice from parent1
    child[a:b+1] = parent1_seq[a:b+1]
    # fill remaining with parent2 order
    p2_iter = [x for x in parent2_seq if x not in child[a:b+1]]
    idx = 0
    for i in range(length):
        if child[i] is None:
            child[i] = p2_iter[idx]
            idx += 1
    return child


def crossover_vrp(parent1: List[List[int]], parent2: List[List[int]], num_vehicles: int) -> List[List[int]]:
    """
    VRP crossover:
    - flatten parents into sequences
    - apply Order Crossover (OX) to produce a child sequence
    - split child sequence into num_vehicles routes via round-robin
    """
    seq1 = flatten_chromosome(parent1)
    seq2 = flatten_chromosome(parent2)
    if set(seq1) != set(seq2):
        # if parents reference different sets, fallback to parent1 copy split
        seq = seq1
    else:
        seq = order_crossover_ids(seq1, seq2)

    # split round-robin
    routes = [[] for _ in range(num_vehicles)]
    for idx, cid in enumerate(seq):
        routes[idx % num_vehicles].append(cid)
    return routes

