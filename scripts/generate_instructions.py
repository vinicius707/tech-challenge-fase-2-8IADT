#!/usr/bin/env python3
import sys
import os
import json
from src.llm.adapter import LLMAdapter
from src.viz import map as viz_map
from src.ga import representation

def load_geojson(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

def summarize_routes(decoded_routes):
    lines = []
    for vid, route in enumerate(decoded_routes):
        lines.append(f"Vehicle {vid}: {len(route)} stops, load={sum(p.get('volume',0) for p in route)}")
        for idx, p in enumerate(route, start=1):
            lines.append(f"  {idx}) id:{p['id']} coord:({p['lat']},{p['lon']}) priority:{p.get('priority','')}")
    return "\n".join(lines)

def main(out_dir: str, prompt_path: str = "experiments/prompts/route_instructions_prompt.txt"):
    geojson_path = os.path.join(out_dir, "routes.geojson")
    if not os.path.exists(geojson_path):
        print("routes.geojson not found in", out_dir)
        sys.exit(1)

    points = representation.parse_instance_csv("data/instances/hospital_points.csv")
    lookup = representation.build_points_lookup(points)

    # read geojson and reconstruct decoded routes (we can map ids back)
    gj = load_geojson(geojson_path)
    decoded = []
    for feat in gj.get("features", []):
        seq = feat.get("properties", {}).get("sequence", [])
        decoded.append([lookup[int(cid)] for cid in seq])

    route_summary = summarize_routes(decoded)

    prompt_template = None
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as fh:
            prompt_template = fh.read()

    adapter = LLMAdapter()
    instructions = adapter.generate_instructions(route_summary, prompt_template=prompt_template)

    out_path = os.path.join(out_dir, "instruction.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(instructions)

    print("Wrote instruction:", out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_instructions.py <out_dir> [prompt_path]")
        sys.exit(1)
    out = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "experiments/prompts/route_instructions_prompt.txt"
    main(out, prompt)

