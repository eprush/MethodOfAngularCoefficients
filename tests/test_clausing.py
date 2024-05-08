from tests import t, coeffs


def test_clausing():
    k = t.calc_clausing(coeffs)
    assert 0.0 < k < 1.0
    min_degree, max_degree = -6, -1
    assert 10 ** min_degree < k < 10**max_degree
