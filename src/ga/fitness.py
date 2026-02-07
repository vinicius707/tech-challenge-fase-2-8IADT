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


def fitness_for_chromosome(decoded_routes: List[List[Dict[str, Any]]], weights: Dict[str, float], depot: Dict[str, Any]=None) -> float:
    """
    Compute a weighted fitness: lower is better.
    weights: dict with keys 'distance', 'capacity_penalty', 'priority_penalty'
    For now, capacity and priority penalties are placeholders (0).
    """
    total_distance = 0.0
    for route in decoded_routes:
        total_distance += total_distance_for_route(route, depot=depot)

    # Placeholder penalties (to be implemented)
    capacity_penalty = 0.0
    priority_penalty = 0.0

    return weights.get('distance', 1.0) * total_distance + weights.get('capacity_penalty', 0.0) * capacity_penalty + weights.get('priority_penalty', 0.0) * priority_penalty

