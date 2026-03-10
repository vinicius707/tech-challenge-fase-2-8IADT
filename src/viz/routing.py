"""
Routing via OSRM (Open Source Routing Machine) to get road-following paths.
Uses public demo server; falls back to straight line if unavailable.
"""
from typing import List, Tuple, Optional

OSRM_BASE = "https://router.project-osrm.org"


def route_via_roads(latlons: List[Tuple[float, float]]) -> Optional[List[Tuple[float, float]]]:
    """
    Fetch driving route that follows streets from OSRM.
    Args:
        latlons: List of (lat, lon) tuples (waypoints in order)
    Returns:
        List of (lat, lon) for the road-following path, or None if OSRM fails.
    """
    if len(latlons) < 2:
        return [(latlons[0][0], latlons[0][1])] if latlons else []
    coords_str = ";".join(f"{lon},{lat}" for lat, lon in latlons)
    url = f"{OSRM_BASE}/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
    try:
        import requests
        r = requests.get(url, timeout=15, headers={"User-Agent": "TechChallenge-VRP/1.0"})
        r.raise_for_status()
        data = r.json()
        routes = data.get("routes", [])
        if not routes:
            return None
        coords = routes[0].get("geometry", {}).get("coordinates", [])
        if not coords:
            return None
        return [(c[1], c[0]) for c in coords]
    except Exception:
        return None
