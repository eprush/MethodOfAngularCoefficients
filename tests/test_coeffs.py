import numpy as np
from tube import Tube
from math import isclose
from decimal import Decimal

t = Tube(1, 1, 1, Decimal(0.05))
sep = t.separator
coeffs = t.calc_angular_coeffs()


def test_isolation():
    for i in range(len(sep)):
        sums = np.sum(coeffs[i])
        assert isclose(sums, 1.0), f"Should be equal one; {i}-th side"


def test_mutuality():
    num = len(sep)
    for i in range(num):
        for j in range(num):
            assert isclose(coeffs[i][j], coeffs[j][i]), f"Should be equal; {i}-th and {j}-th sides"
