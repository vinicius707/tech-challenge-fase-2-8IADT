from typing import List, Dict, Any
import json
import os

def routes_to_geojson(decoded_routes: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Convert decoded routes (list of routes of point dicts) into a GeoJSON FeatureCollection.
    Each route is represented as a LineString feature with properties.
    """
    features = []
    for vid, route in enumerate(decoded_routes):
        coords = [[p['lon'], p['lat']] for p in route]
        props = {
            "vehicle_id": vid,
            "sequence": [p['id'] for p in route],
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

    m = folium.Map(location=center, zoom_start=12)
    colors = ["blue", "green", "red", "orange", "purple", "brown"]
    for vid, route in enumerate(decoded_routes):
        latlons = [(p['lat'], p['lon']) for p in route]
        if not latlons:
            continue
        folium.PolyLine(latlons, color=colors[vid % len(colors)], weight=4, tooltip=f"Vehicle {vid}").add_to(m)
        for idx, p in enumerate(route):
            folium.CircleMarker(location=(p['lat'], p['lon']), radius=4, popup=f"id:{p['id']} pri:{p.get('priority','')}", color=colors[vid % len(colors)]).add_to(m)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    m.save(path)
