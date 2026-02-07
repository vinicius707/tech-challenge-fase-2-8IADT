from typing import List, Dict, Any, Tuple
import csv
import os


def parse_instance_csv(path: str) -> List[Dict[str, Any]]:
    """
    Parse a CSV instance file with columns:
      id, lat, lon, priority, volume, notes

    Returns a list of dicts with keys: id (int), lat (float), lon (float),
    priority (str), volume (float), notes (str)
    """
    points = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"Instance file not found: {path}")

    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            points.append({
                'id': int(row['id']),
                'lat': float(row['lat']),
                'lon': float(row['lon']),
                'priority': row.get('priority', '').strip(),
                'volume': float(row.get('volume') or 0.0),
                'notes': row.get('notes', '').strip()
            })

    return points


def encode_chromosome(points: List[Dict[str, Any]], num_vehicles: int) -> List[List[int]]:
    """
    Simple encoder: distribute points round-robin into num_vehicles routes.
    Returns a chromosome represented as a list of routes, each route is a list of point ids.
    This is a placeholder; later replace with heuristics (savings, nearest neighbor).
    """
    if num_vehicles < 1:
        raise ValueError('num_vehicles must be >= 1')

    routes: List[List[int]] = [[] for _ in range(num_vehicles)]
    for idx, p in enumerate(points):
        routes[idx % num_vehicles].append(p['id'])
    return routes


def decode_chromosome(routes: List[List[int]], points_lookup: Dict[int, Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """
    Decode chromosome (list of routes of ids) into detailed routes with point dicts.
    """
    decoded = []
    for route in routes:
        decoded.append([points_lookup[rid] for rid in route])
    return decoded


def build_points_lookup(points: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    return {p['id']: p for p in points}

