from src.ga import fitness

def test_haversine_known():
    # Paris (48.8566, 2.3522) to London (51.5074, -0.1278) ~ 343 km
    paris = {"lat": 48.8566, "lon": 2.3522}
    london = {"lat": 51.5074, "lon": -0.1278}
    d = fitness.haversine_distance(paris, london)
    assert 330 <= d <= 360


def test_total_distance_with_depot():
    depot = {"lat": 0.0, "lon": 0.0}
    p1 = {"lat": 0.1, "lon": 0.0}
    route = [p1]
    dist = fitness.total_distance_for_route(route, depot=depot)
    single = fitness.haversine_distance(depot, p1)
    assert abs(dist - 2 * single) < 1e-6


def test_fitness_distance_only():
    depot = {"lat": 0.0, "lon": 0.0}
    p1 = {"lat": 0.0, "lon": 0.1}
    p2 = {"lat": 0.1, "lon": 0.1}
    decoded = [[p1, p2]]
    weights = {"distance": 1.0, "capacity_penalty": 0.0, "priority_penalty": 0.0}
    f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
    # should equal total distance for that single route
    expected = fitness.total_distance_for_route([p1, p2], depot=depot)
    assert abs(f - expected) < 1e-6

