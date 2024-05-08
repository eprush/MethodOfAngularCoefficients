from tube import calc_elementary
from math import isclose
from decimal import Decimal
from tests import sep
import numpy as np
import random


def test_sphere():
    r = Decimal(str(random.uniform(0.0, 10.0)))
    s = Decimal(str(random.uniform(0.0, 0.1)))
    x, y = random.uniform(0.0, float(r)), random.uniform(0.0, float(r))
    x, y = Decimal(str(x)) / Decimal(2).sqrt(), Decimal(str(y)) / Decimal(2).sqrt()
    z = (r ** 2 - x ** 2 - y ** 2).sqrt()
    center = np.array([x, y, z])  # square on the sphere
    emitter = list(map(str, np.zeros(3)))
    emitter = np.array(list(map(Decimal, emitter)))  # center of the sphere
    normal_i = (center - emitter) / np.linalg.norm(center - emitter)
    normal_j = center / r
    my_ac = calc_elementary(emitter, center, normal_i, normal_j, s)
    actual_ac = s / Decimal(str(4 * np.pi)) / r ** 2
    assert isclose(my_ac, actual_ac), f"{emitter=}"


def test_cube_isolation():
    emitter = np.random.rand(3)
    emitter = list(map(str, emitter))
    emitter = np.array(list(map(Decimal, emitter)))  # point into the cube
    res = Decimal(0)
    for j, collector in enumerate(sep):
        collector = np.array(collector)  # square on the cube
        normal_i = (emitter - collector) / np.linalg.norm(emitter - collector)
        res += calc_elementary(emitter, collector, normal_i, sep.find_normal(j), sep.step_size ** 2)
    assert isclose(1.0, float(res)), f"{emitter=}"
