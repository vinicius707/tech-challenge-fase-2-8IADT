from typing import List, Dict, Any, Optional
import json
import os

try:
    from .routing import route_via_roads
except ImportError:
    route_via_roads = None


def _compute_depot(decoded_routes: List[List[Dict[str, Any]]]) -> Dict[str, float]:
    """
    Compute depot as centroid. For single-point routes, offset slightly so the
    round-trip path (depot->stop->depot) is visible instead of a degenerate point.
    """
    lats, lons = [], []
    for route in decoded_routes:
        for p in route:
            lats.append(p['lat'])
            lons.append(p['lon'])
    if not lats or not lons:
        return {"lat": 0.0, "lon": 0.0}
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    # Single point or all same: offset depot ~0.01° (~1 km) so path is visible
    if len(lats) == 1 or (max(lats) - min(lats) < 1e-6 and max(lons) - min(lons) < 1e-6):
        return {"lat": center_lat + 0.008, "lon": center_lon + 0.008}
    return {"lat": center_lat, "lon": center_lon}


def _route_with_depot(route: List[Dict[str, Any]], depot: Dict[str, float]) -> List[Dict[str, Any]]:
    """Prepend and append depot to show full round-trip path."""
    if not route:
        return []
    return [depot] + route + [depot]


def routes_to_geojson(decoded_routes: List[List[Dict[str, Any]]], depot: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Convert decoded routes (list of routes of point dicts) into a GeoJSON FeatureCollection.
    Each route is represented as a LineString feature. Depot is included for full path.
    """
    depot = depot or _compute_depot(decoded_routes)
    features = []
    for vid, route in enumerate(decoded_routes):
        full_route = _route_with_depot(route, depot)
        latlons = [(p['lat'], p['lon']) for p in full_route]
        if route_via_roads and len(latlons) >= 2:
            road = route_via_roads(latlons)
            coords = [[lon, lat] for lat, lon in (road or latlons)]
        else:
            coords = [[p['lon'], p['lat']] for p in full_route]
        props = {
            "vehicle_id": vid,
            "sequence": [p['id'] for p in route],  # customer ids only
            "load": sum(p.get('volume', 0.0) for p in route),
            "priorities": [p.get('priority', '') for p in route],
        }
        feature = {
            "type": "Feature",
            "properties": props,
            "geometry": {"type": "LineString", "coordinates": coords},
        }
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}


def save_geojson(geojson_obj: Dict[str, Any], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(geojson_obj, fh, indent=2, ensure_ascii=False)


def generate_simple_html_map(decoded_routes: List[List[Dict[str, Any]]], path: str, center: List[float]=None):
    """
    Generate a minimal interactive map using folium if available; otherwise write a placeholder HTML.
    """
    try:
        import folium
    except Exception:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("<html><body><h3>Folium não disponível — instale folium para visualizar mapas.</h3></body></html>")
        return

    if center is None:
        # compute average lat/lon
        lats = []
        lons = []
        for route in decoded_routes:
            for p in route:
                lats.append(p['lat'])
                lons.append(p['lon'])
        if lats and lons:
            center = [sum(lats)/len(lats), sum(lons)/len(lons)]
        else:
            center = [0, 0]

    depot = _compute_depot(decoded_routes)
    m = folium.Map(location=center, zoom_start=12)
    folium.CircleMarker(location=(depot['lat'], depot['lon']), radius=6, popup="Depósito", color="black", fill=True).add_to(m)
    colors = ["blue", "green", "red", "orange", "purple", "brown"]
    for vid, route in enumerate(decoded_routes):
        full_path = _route_with_depot(route, depot)
        latlons = [(p['lat'], p['lon']) for p in full_path]
        if len(latlons) < 2:
            continue
        # Use OSRM for road-following path; fallback to straight line
        if route_via_roads:
            road_coords = route_via_roads(latlons)
            draw_coords = road_coords if road_coords else latlons
        else:
            draw_coords = latlons
        folium.PolyLine(draw_coords, color=colors[vid % len(colors)], weight=4, tooltip=f"Vehicle {vid}").add_to(m)
        for p in route:
            folium.CircleMarker(location=(p['lat'], p['lon']), radius=4, popup=f"id:{p['id']} pri:{p.get('priority','')}", color=colors[vid % len(colors)]).add_to(m)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    m.save(path)
