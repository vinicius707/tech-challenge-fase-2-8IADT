from typing import List, Dict, Any, Tuple
import math
import random
from .fitness import haversine_distance


def nearest_neighbor_init(points: List[Dict[str, Any]], num_vehicles: int, depot: Dict[str, Any]=None) -> List[List[int]]:
    """
    Simple nearest neighbor initializer:
    - choose seeds by picking the farthest points spaced across the list
    - for each route, grow by adding nearest unvisited point until all assigned
    """
    ids = [p['id'] for p in points]
    lookup = {p['id']: p for p in points}
    unvisited = set(ids)
    routes: List[List[int]] = [[] for _ in range(num_vehicles)]

    # choose seeds: pick first num_vehicles points (or spaced)
    if not ids:
        return routes
    step = max(1, len(ids) // num_vehicles)
    seeds = [ids[i*step] for i in range(num_vehicles)]
    for i, s in enumerate(seeds):
        if s in unvisited:
            routes[i].append(s)
            unvisited.remove(s)

    # grow routes by nearest neighbor
    while unvisited:
        for r in routes:
            if not unvisited:
                break
            # determine last point location
            last_id = r[-1] if r else None
            last_point = lookup[last_id] if last_id is not None else depot or points[0]
            # find nearest unvisited
            nearest = min(unvisited, key=lambda uid: haversine_distance(last_point, lookup[uid]))
            r.append(nearest)
            unvisited.remove(nearest)
    return routes


def clarke_wright_savings(points: List[Dict[str, Any]], num_vehicles: int, depot: Dict[str, Any]=None) -> List[List[int]]:
    """
    Simplified Clarke-Wright savings:
    - start with each node in its own route
    - compute savings and merge routes greedily until number of routes == num_vehicles
    Note: does not enforce capacity constraints in this simplified version.
    """
    if not points:
        return [[] for _ in range(num_vehicles)]
    if depot is None:
        depot = {"lat": points[0]['lat'], "lon": points[0]['lon']}
    lookup = {p['id']: p for p in points}
    routes = {p['id']: [p['id']] for p in points}

    # compute savings
    ids = list(lookup.keys())
    savings: List[Tuple[float, int, int]] = []
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            a = lookup[ids[i]]
            b = lookup[ids[j]]
            s = haversine_distance(depot, a) + haversine_distance(depot, b) - haversine_distance(a, b)
            savings.append((s, ids[i], ids[j]))
    savings.sort(reverse=True, key=lambda x: x[0])

    # greedy merge
    for s, i_id, j_id in savings:
        # find routes containing i and j
        ri = None
        rj = None
        for key, r in routes.items():
            if i_id in r:
                ri = key
            if j_id in r:
                rj = key
        if ri is None or rj is None or ri == rj:
            continue
        # merge rj into ri
        routes[ri] = routes[ri] + routes[rj]
        del routes[rj]
        if len(routes) <= num_vehicles:
            break

    # convert to list and if fewer than num_vehicles, add empty routes
    result = list(routes.values())
    while len(result) < num_vehicles:
        result.append([])
    # if more, truncate (should not happen)
    if len(result) > num_vehicles:
        # try to merge small routes into first ones
        flat = [cid for r in result for cid in r]
        result = [[] for _ in range(num_vehicles)]
        for idx, cid in enumerate(flat):
            result[idx % num_vehicles].append(cid)
    return result
