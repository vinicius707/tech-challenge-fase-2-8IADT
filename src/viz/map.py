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


def generate_simple_html_map(decoded_routes: List[List[Dict[str, Any]]], path: str, center: Optional[List[float]]=None):
    """
    Generate an enhanced interactive map with dynamic zoom and clear route visualization.
    """
    try:
        import folium
    except Exception:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("<html><body><h3>Folium não disponível — instale folium para visualizar mapas.</h3></body></html>")
        return

    all_points = []
    depot = _compute_depot(decoded_routes)
    all_points.append([depot['lat'], depot['lon']])
    
    for route in decoded_routes:
        for p in route:
            all_points.append([p['lat'], p['lon']])

    if not all_points:
        center = [0, 0]
    elif center is None:
        center = [sum(p[0] for p in all_points)/len(all_points), sum(p[1] for p in all_points)/len(all_points)]

    # Use a cleaner, professional tile set
    m = folium.Map(location=center, zoom_start=13, tiles="cartodbpositron")

    # Clearer Depot marker
    folium.Marker(
        location=(depot['lat'], depot['lon']),
        popup="<b>Depósito Central</b>",
        tooltip="Início/Fim das Rotas",
        icon=folium.Icon(color="black", icon="warehouse", prefix="fa")
    ).add_to(m)

    # More vibrant and distinct color palette
    colors = ["#2563eb", "#16a34a", "#dc2626", "#d97706", "#7c3aed", "#0891b2", "#be185d", "#4f46e5"]
    
    for vid, route in enumerate(decoded_routes):
        color = colors[vid % len(colors)]
        full_path = _route_with_depot(route, depot)
        latlons = [(p['lat'], p['lon']) for p in full_path]
        
        if len(latlons) < 2:
            continue
            
        # Draw the route line with improved styling
        if route_via_roads:
            road_coords = route_via_roads(latlons)
            draw_coords = road_coords if road_coords else latlons
        else:
            draw_coords = latlons
            
        folium.PolyLine(
            draw_coords, 
            color=color, 
            weight=5, 
            opacity=0.75,
            tooltip=f"Veículo {vid}",
            popup=f"<b>Rota Veículo {vid}</b><br/>Paradas: {len(route)}"
        ).add_to(m)

        # Draw stop markers with sequence numbers
        for idx, p in enumerate(route):
            folium.CircleMarker(
                location=(p['lat'], p['lon']),
                radius=7,
                popup=f"<b>Parada {idx+1}</b><br/>ID: {p['id']}<br/>Prioridade: {p.get('priority','')}",
                tooltip=str(idx+1),
                color=color,
                fill=True,
                fill_color="white",
                fill_opacity=1.0,
                weight=3
            ).add_to(m)
            
            # Simple text overlay for sequence (optional, might be too busy)
            # For now, tooltips provide the sequence number clearly.

    # Dynamic zooming: Automatically fit all routes in view
    if all_points:
        m.fit_bounds(all_points, padding=(50, 50))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    m.save(path)
