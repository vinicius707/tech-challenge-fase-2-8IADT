from typing import List, Dict, Any
import math

def haversine_distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    """
    Approximate Haversine distance (in kilometers) between two points with lat/lon.
    """
    lat1, lon1 = math.radians(a['lat']), math.radians(a['lon'])
    lat2, lon2 = math.radians(b['lat']), math.radians(b['lon'])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    r = 6371.0
    hav = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * r * math.asin(math.sqrt(hav))


def total_distance_for_route(route: List[Dict[str, Any]], depot: Dict[str, Any]=None) -> float:
    """
    Sum distances along a route; if depot provided, assume route starts/ends at depot.
    """
    if not route:
        return 0.0
    dist = 0.0
    if depot:
        dist += haversine_distance(depot, route[0])
    for i in range(len(route)-1):
        dist += haversine_distance(route[i], route[i+1])
    if depot:
        dist += haversine_distance(route[-1], depot)
    return dist


def _priority_weight(priority: str) -> float:
    """Priority multiplier: critical=3, high/alta=2, medium/média=1, low/baixa=0."""
    p = str(priority or "").lower().strip()
    if p in ("critical", "crítica", "critico", "crítico"):
        return 3.0
    if p in ("high", "alta"):
        return 2.0
    if p in ("medium", "média", "media"):
        return 1.0
    return 0.0


def fitness_for_chromosome(decoded_routes: List[List[Dict[str, Any]]], weights: Dict[str, Any], depot: Dict[str, Any]=None) -> float:
    """
    Compute a weighted fitness: lower is better.
    weights: distance, capacity_penalty, priority_penalty, vehicle_capacity (or vehicle_capacities list),
             vehicle_autonomies (list of km per vehicle).
    """
    total_distance = 0.0
    route_distances = []
    for route in decoded_routes:
        d = total_distance_for_route(route, depot=depot)
        total_distance += d
        route_distances.append(d)

    # Capacity penalty: per-vehicle capacity
    capacities = weights.get("vehicle_capacities")
    if capacities is None:
        capacities = [weights.get("vehicle_capacity")] * len(decoded_routes)
    capacity_penalty = 0.0
    for i, route in enumerate(decoded_routes):
        cap = capacities[i] if i < len(capacities) else (capacities[-1] if capacities else None)
        if cap is not None:
            load = sum(p.get("volume", 0.0) for p in route)
            if load > cap:
                capacity_penalty += (load - cap)

    # Autonomy penalty: per-vehicle max distance
    autonomies = weights.get("vehicle_autonomies", [])
    autonomy_penalty = 0.0
    for i, dist in enumerate(route_distances):
        aut = autonomies[i] if i < len(autonomies) else (autonomies[-1] if autonomies else None)
        if aut is not None and dist > aut:
            autonomy_penalty += (dist - aut)

    # Priority penalty: critical=3, high=2, medium=1 (position index weighted)
    priority_penalty = 0.0
    for route in decoded_routes:
        for idx, p in enumerate(route):
            w = _priority_weight(p.get("priority", ""))
            if w > 0:
                priority_penalty += idx * w

    return (
        weights.get("distance", 1.0) * total_distance
        + weights.get("capacity_penalty", 0.0) * capacity_penalty
        + weights.get("autonomy_penalty", 1.0) * autonomy_penalty
        + weights.get("priority_penalty", 0.0) * priority_penalty
    )

