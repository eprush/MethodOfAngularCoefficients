import numpy as np
from math import isclose
from tests import sep, coeffs

num = len(sep)


def test_isolation():
    eps = 10 ** (-2)
    for i in range(num):
        assert 1 - eps < np.sum(coeffs[i]) < 1 + eps, f"Incorrect value with {i}-th cell"


def test_mutuality():
    for i in range(num):
        for j in range(num):
            assert isclose(coeffs[i][j], coeffs[j][i]), f"Should be equal; {i}-th and {j}-th cells"
