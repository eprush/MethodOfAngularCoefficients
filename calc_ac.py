from decimal import Decimal
import numpy as np

Center = np.ndarray


def calc_elementary(center_i: Center, center_j: Center, normal_i: Center, normal_j: Center, F_j: Decimal) -> Decimal:
    # F_j - the area of one collector cell
    r_vector = center_i - center_j
    r = np.linalg.norm(r_vector)
    if not (r > 0.0):
        return Decimal("0.0")
    n_i, n_j = np.linalg.norm(normal_i), np.linalg.norm(normal_j)
    cos_i = abs(np.dot(normal_i, r_vector)) / (r * n_i)
    cos_j = abs(np.dot(normal_j, r_vector)) / (r * n_j)
    return cos_i * cos_j / (Decimal(str(4 * np.pi)) * r ** 2) * F_j
