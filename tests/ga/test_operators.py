from src.ga import operators


def flatten(chrom):
    return [c for route in chrom for c in route]


def test_relocate_preserves_customers():
    chrom = [[1, 2, 3], [4, 5], [6]]
    new = operators.relocate(chrom)
    assert sorted(flatten(new)) == sorted(flatten(chrom))
    # all customers present and count equal
    assert len(flatten(new)) == len(flatten(chrom))


def test_swap_preserves_customers():
    chrom = [[1, 2, 3], [4, 5, 6]]
    new = operators.swap(chrom)
    assert sorted(flatten(new)) == sorted(flatten(chrom))
    assert len(flatten(new)) == len(flatten(chrom))


def test_two_opt_reverses_segment():
    route = [1, 2, 3, 4, 5]
    new_route = operators.two_opt(route)
    assert sorted(new_route) == sorted(route)
    assert len(new_route) == len(route)

