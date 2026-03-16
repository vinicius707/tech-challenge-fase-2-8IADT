from src.ga import operators


def flatten(chrom):
    return [c for route in chrom for c in route]


def test_crossover_vrp_preserves_customers():
    p1 = [[1,2,3],[4,5],[6,7]]
    p2 = [[6,2,5],[1,3,4],[7]]
    child = operators.crossover_vrp(p1, p2, num_vehicles=3)
    # validate same set of customers
    assert set(flatten(child)) == set(flatten(p1)) == set(flatten(p2))
    # no duplicates
    assert len(flatten(child)) == len(set(flatten(child)))

