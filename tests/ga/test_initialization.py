from src.ga import initialization, representation


def test_nearest_neighbor_init_covers_all():
    points = representation.parse_instance_csv("data/instances/hospital_points.csv")
    routes = initialization.nearest_neighbor_init(points, num_vehicles=3)
    ids = [p['id'] for route in [r for r in routes] for p in [next(filter(lambda x: x['id']==cid, points)) for cid in route]]
    assert set(ids) == set([p['id'] for p in points])


def test_clarke_wright_init_covers_all():
    points = representation.parse_instance_csv("data/instances/hospital_points.csv")
    routes = initialization.clarke_wright_savings(points, num_vehicles=3)
    ids = [cid for route in routes for cid in route]
    assert set(ids) == set([p['id'] for p in points])

