from src.ga import fitness

def test_capacity_penalty_applied():
    depot = {"lat": 0.0, "lon": 0.0}
    # two points, large volumes causing overload on single vehicle
    p1 = {"lat": 0.0, "lon": 0.0, "volume": 80.0, "priority": "medium"}
    p2 = {"lat": 0.01, "lon": 0.01, "volume": 50.0, "priority": "low"}
    decoded = [[p1, p2]]  # one route only
    weights = {"distance": 0.0, "capacity_penalty": 1.0, "priority_penalty": 0.0, "vehicle_capacity": 100.0}
    f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
    # load = 130 -> overload 30 -> capacity_penalty should contribute 30
    assert abs(f - 30.0) < 1e-6


def test_priority_penalty_applied():
    depot = {"lat": 0.0, "lon": 0.0}
    # high priority item late in route (index 2)
    p1 = {"lat": 0.0, "lon": 0.0, "volume": 1.0, "priority": "low"}
    p2 = {"lat": 0.0, "lon": 0.01, "volume": 1.0, "priority": "low"}
    p3 = {"lat": 0.0, "lon": 0.02, "volume": 1.0, "priority": "high"}
    decoded = [[p1, p2, p3]]
    weights = {"distance": 0.0, "capacity_penalty": 0.0, "priority_penalty": 2.0, "vehicle_capacity": 100.0}
    f = fitness.fitness_for_chromosome(decoded, weights, depot=depot)
    # priority penalty = index 2 * weight 2.0 = 4.0
    assert abs(f - 4.0) < 1e-6

