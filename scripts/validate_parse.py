#!/usr/bin/env python3
import json
from src.ga import representation

def main():
    path = "data/instances/hospital_points.csv"
    points = representation.parse_instance_csv(path)
    out = {"n_points": len(points), "sample": points[:3]}
    with open("experiments/validate_parse.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("Wrote experiments/validate_parse.json")

if __name__ == '__main__':
    main()

