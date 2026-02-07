from src.ga import representation

def test_parse_and_encode_decode():
    points = representation.parse_instance_csv("data/instances/hospital_points.csv")
    lookup = representation.build_points_lookup(points)
    chrom = representation.encode_chromosome(points, num_vehicles=3)
    decoded = representation.decode_chromosome(chrom, lookup)
    # ensure all points covered exactly once
    ids = [p['id'] for route in decoded for p in route]
    assert len(ids) == len(set(ids)) == len(points)

