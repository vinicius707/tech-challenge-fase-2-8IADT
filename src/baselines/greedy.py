"""
Nearest-neighbor greedy baseline for VRP.
Uses the same fitness evaluation as the GA for fair comparison.
"""
from typing import List, Dict, Any, Optional

from src.ga import representation, fitness
from src.ga.initialization import nearest_neighbor_init


def _compute_depot(points: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute depot as centroid of all points."""
    if not points:
        return {"lat": 0.0, "lon": 0.0}
    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]
    return {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}


def run_nearest_neighbor(
    points: List[Dict[str, Any]],
    num_vehicles: int = 3,
    weights: Optional[Dict[str, Any]] = None,
    depot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Run nearest-neighbor greedy baseline.
    Returns dict with routes (chromosome), decoded routes, fitness, and total_distance_km.
    """
    if weights is None:
        weights = {
            "distance": 1.0,
            "capacity_penalty": 1.0,
            "priority_penalty": 1.0,
            "autonomy_penalty": 1.0,
            "vehicle_capacity": 100.0,
        }

    if not points:
        return {"routes": [[] for _ in range(num_vehicles)], "fitness": float("inf"), "total_distance_km": 0.0}

    depot = depot or _compute_depot(points)
    lookup = representation.build_points_lookup(points)

    # nearest_neighbor_init returns List[List[int]]
    routes = nearest_neighbor_init(points, num_vehicles, depot=depot)
    decoded = representation.decode_chromosome(routes, lookup)

    f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
    total_km = sum(fitness.total_distance_for_route(r, depot=depot) for r in decoded)

    return {
        "routes": routes,
        "decoded": decoded,
        "fitness": f,
        "total_distance_km": round(total_km, 2),
        "depot": depot,
    }
