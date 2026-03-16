#!/usr/bin/env python3
import json
import sys
from src.ga import representation

def main():
    path = "data/instances/hospital_points.csv"
    try:
        points = representation.parse_instance_csv(path)
    except Exception as e:
        print("PARSE_ERROR", str(e))
        sys.exit(1)

    lookup = representation.build_points_lookup(points)
    chrom = representation.encode_chromosome(points, num_vehicles=3)
    decoded = representation.decode_chromosome(chrom, lookup)

    out = {
        "n_points": len(points),
        "chromosome": chrom,
        "decoded_first_route_sample": decoded[0] if decoded else []
    }

    with open("experiments/validate_repr.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    print("Validation successful. Wrote experiments/validate_repr.json")

if __name__ == "__main__":
    main()

