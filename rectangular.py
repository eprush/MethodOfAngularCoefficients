import os
import math
import numpy as np


# УГЛОВЫЕ КОЭФФИЦИЕНТЫ
def scalar_prod(v_1, v_2):
    v_1, v_2 = np.array(v_1), np.array(v_2)
    return np.dot(v_1, v_2)


def module(v):
    return math.sqrt(scalar_prod(v, v))


def elementary(center_i: list, center_j: list, normal_i: list, normal_j: list, F_j):
    # F_j - площадь одной ячейки коллектора.
    center_i, center_j = np.array(center_i), np.array(center_j)

    r = module(center_i - center_j)
    n_i, n_j = module(normal_i), module(normal_j)

    cos_i = abs(scalar_prod(normal_i, center_j - center_i)) / (r * n_i)
    cos_j = abs(scalar_prod(normal_j, center_i - center_j)) / (r * n_j)
    return cos_i * cos_j / (math.pi * r ** 2) * F_j


def local(center_i, centers_j, normal_i, normal_j, F_j):
    return sum([elementary(center_i, center, normal_i, normal_j, F_j) for center in centers_j])


def emitter_to_collector(centers_i, centers_j, normal_i, normal_j, F_i, F_j):
    # F_i - площадь одной ячейки эмиттера.
    return sum([local(center, centers_j, normal_i, normal_j, F_j) for center in centers_i]) * F_i


# РАЗБИЕНИЕ
def euclid(num_1, num_2):
    while num_1 != num_2:
        if num_1 > num_2:
            num_1 -= num_2
        else:
            num_2 -= num_1
    return num_1


# ф-ция находит минимальное количество квадратов
# с одинаковой площадью, на которое можно разбить
# данный прямоугольник
def search_squares(a: int, b: int) -> int:
    gcd = euclid(a, b)  # НОД
    return int(a * b / gcd)


# ф-ция ищет оптимальное кол-во квадратов
# в зависимости от введенного кол-ва
def optimal_squares(a, b, num):
    min_num = search_squares(a, b)
    n = num // (4 * min_num)
    return 4 * min_num * n if n > 0 else min_num


# функции разбиения каждой отдельной поверхности на ячейки.
# 1-входное, 2-выходное сечения.
# 3-верхняя, 5-нижняя грани.
# если смотреть в направлении от 1 к 2, то
# 3,4,5 и 6 грани пронумерованы по часовой стрелке.
def breaking_1(a, b, num, s=0) -> list:
    # a - вдоль x, b - вдоль z, s - вдоль y
    num = optimal_squares(a, b, num)

    square_side = math.sqrt(a * b / num)
    l_1 = int(a / square_side)
    l_2 = int(b / square_side)
    res = []
    for i in range(l_1):
        x = a / (2 * l_1) + a / l_1 * i
        for j in range(l_2):
            z = b / (2 * l_2) + b / l_2 * j
            center = [x, 0, z]
            res.append(center)
    return res


def breaking_2(a, b, num, s) -> list:
    res = []
    num = optimal_squares(a, b, num)

    square_side = math.sqrt(a * b / num)
    l_1 = int(a / square_side)
    l_2 = int(b / square_side)
    for i in range(l_1):
        x = a / (2 * l_1) + a / l_1 * i
        for j in range(l_2):
            z = b / (2 * l_2) + b / l_2 * j
            center = [x, s, z]
            res.append(center)
    return res


def breaking_3(a, b, num, s) -> list:
    res = []
    num = optimal_squares(a, s, num)

    square_side = math.sqrt(a * s / num)
    l_1 = int(a / square_side)
    l_2 = int(s / square_side)
    for i in range(l_1):
        x = a / (2 * l_1) + a / l_1 * i
        for j in range(l_2):
            y = s / (2 * l_2) + s / l_2 * j
            center = [x, y, b]
            res.append(center)
    return res


def breaking_4(a, b, num, s) -> list:
    res = []
    num = optimal_squares(s, b, num)

    square_side = math.sqrt(s * b / num)
    l_1 = int(s / square_side)
    l_2 = int(b / square_side)
    for i in range(l_1):
        y = s / (2 * l_1) + s / l_1 * i
        for j in range(l_2):
            z = b / (2 * l_2) + b / l_2 * j
            center = [0, y, z]
            res.append(center)
    return res


def breaking_5(a, b, num, s) -> list:
    res = []
    num = optimal_squares(a, s, num)

    square_side = math.sqrt(a * s / num)
    l_1 = int(a / square_side)
    l_2 = int(s / square_side)
    for i in range(l_1):
        x = a / (2 * l_1) + a / l_1 * i
        for j in range(l_2):
            y = s / (2 * l_2) + s / l_2 * j
            center = [x, y, 0]
            res.append(center)
    return res


def breaking_6(a, b, num, s) -> list:
    res = []
    num = optimal_squares(s, b, num)

    square_side = math.sqrt(s * b / num)
    l_1 = int(s / square_side)
    l_2 = int(b / square_side)
    for i in range(l_1):
        y = s / (2 * l_1) + s / l_1 * i
        for j in range(l_2):
            z = b / (2 * l_2) + b / l_2 * j
            center = [a, y, z]
            res.append(center)
    return res


# площади "уникальных" поверхностей - area_1 == area_2 итд
def area_1(a, b, s):
    return a * b


def area_3(a, b, s):
    return a * s


def area_4(a, b, s):
    return s * b


# ПРОВОДИМОСТЬ
# ф-ция, заменяющая столбец матрицы
def change_column(A, j: int = 0):
    # A - матрица
    # j - номер изменяемого столбца
    new_A = A.copy()
    for i in range(len(new_A)):
        if i:
            new_A[i][j] = 0
        else:
            new_A[i][j] = 1
    return new_A


class Rectangular:
    def __init__(self, a, b, L):
        self.a = a
        self.b = b
        self.L = L
        self.normals = [[0, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 1], [1, 0, 0]]
        self.breaking = [breaking_1, breaking_2, breaking_3, breaking_4, breaking_5, breaking_6]
        self.areas = [area_1, area_1, area_3, area_4, area_3, area_4]
        for i in range(6):
            self.areas[i] = self.areas[i](a, b, L)
        return

    def some_pair(self, i, j, num_1, num_2):
        # i - номер эмиттера   от 1 до 6.
        # j - номер коллектора от 1 до 6.
        # num_1, num_2 - на сколько частей разбить
        # эмиттер и коллектор соответсвенно.
        i -= 1  # это - номер эмиттера   в массивах.
        j -= 1  # это - номер коллектора в массивах.

        # параметры коллектора:
        # num_j - число квадратов, на которое
        # удалось разделить коллектор в итоге
        collector = self.breaking[j](self.a, self.b, num_2, self.L)
        num_j     = len(collector)
        normal_j  = self.normals[j]
        cell_j    = self.areas[j] / num_j

        # параметры эмиттера:
        # num_i - число квадратов, на которое
        # удалось разделить эмиттер в итоге
        emitter   = self.breaking[i](self.a, self.b, num_1, self.L)
        num_i     = len(emitter)
        normal_i  = self.normals[i]
        area_i    = self.areas[i]
        cell_i    = area_i / num_i
        return emitter_to_collector(emitter, collector, normal_i, normal_j, cell_i, cell_j) / area_i

    def matrix(self, num_1, num_2):
        res = []  # будущая матрица УК
        line = [0] * 7  # текущий столбец матрицы
        # т.к. УК вида phi_21, phi_31, ..., phi_61
        # не используются в дальнейшем
        for j in range(1, 7):
            # благодаря симметрии УК для граней 5 и 6
            # в качестве коллекторов можно не считать,
            # симметрия учтена при решении системы ур-ний 2.1
            res.append(line)
            line = []
            for i in range(7):
                if i:
                    if i == j:
                        line.append(0)
                    else:
                        line.append(self.some_pair(i, j, num_1, num_2))
                else:
                    line = [0]
        res.append(line)
        # транспонируем, чтобы можно было
        # найти phi_ij = matrix[i][j],
        # а не  phi_ij = matrix[j][i]
        return np.transpose(np.array(res))

    def clausing(self, num_1=10, num_2=10):
        phi = self.matrix(num_1, num_2)
        # СЛУ
        sle = [[1, 0, 0],
               [-phi[1][3], 1 - phi[5][3], -2 * phi[4][3]],
               [-phi[1][4], -2 * phi[3][4], 1 - phi[6][4]]]
        sle = np.array(sle)
        delta = np.linalg.det(sle)
        q = []  # [Q_1, Q_3, Q_4]
        # метод Крамера
        for j in range(3):
            new_sle = change_column(sle, j)
            delta_j = np.linalg.det(new_sle)
            q.append(delta_j / delta)
        res = phi[1][2] * q[0]
        res += 2 * phi[3][2] * q[1]
        res += 2 * phi[4][2] * q[2]
        return res
