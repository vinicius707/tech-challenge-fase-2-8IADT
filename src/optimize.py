import argparse
import csv
import json
import os
import sys
from datetime import datetime


def generate_results(output_dir: str, run_id: str):
    os.makedirs(output_dir, exist_ok=True)
    results_path = os.path.join(output_dir, "results.csv")
    geojson_path = os.path.join(output_dir, "routes.geojson")
    html_path = os.path.join(output_dir, "route_map.html")

    # write a simple CSV with a fake metric
    with open(results_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["run_id", "total_distance", "vehicles", "timestamp"])
        writer.writerow([run_id, 1234.56, 2, datetime.utcnow().isoformat()])

    # write a trivial GeoJSON (LineString) as placeholder
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"vehicle_id": 1, "sequence": [1, 2, 3]},
                "geometry": {"type": "LineString", "coordinates": [[-46.63, -23.55], [-46.62, -23.56], [-46.61, -23.57]]},
            }
        ],
    }
    with open(geojson_path, "w") as f:
        json.dump(feature_collection, f, indent=2)

    # try to generate a folium map; if unavailable, write a simple HTML placeholder
    try:
        import folium

        coords = feature_collection["features"][0]["geometry"]["coordinates"]
        # folium expects [lat, lon]
        latlons = [(c[1], c[0]) for c in coords]
        m = folium.Map(location=latlons[0], zoom_start=13)
        folium.PolyLine(latlons, color="blue", weight=5).add_to(m)
        m.save(html_path)
    except Exception:
        with open(html_path, "w") as f:
            f.write("<html><body><h3>Mapa não disponível (folium não instalado)</h3></body></html>")

    return {"results": results_path, "geojson": geojson_path, "html": html_path}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Runner de exemplo para otimização de rotas (placeholder).")
    parser.add_argument("--config", "-c", help="Arquivo de config (yaml/json) — opcional", default=None)
    parser.add_argument("--output", "-o", help="Diretório de saída (default: experiments/run_001)", default="experiments/run_001")
    args = parser.parse_args(argv)

    run_id = datetime.utcnow().strftime("run_%Y%m%d%H%M%S")
    print(f"Starting example optimize runner; run_id={run_id}")
    if args.config:
        print(f"Using config: {args.config}")

    artifacts = generate_results(args.output, run_id)
    print("Artifacts generated:")
    for k, v in artifacts.items():
        print(f" - {k}: {v}")

    print("Done.")


if __name__ == "__main__":
    main()

