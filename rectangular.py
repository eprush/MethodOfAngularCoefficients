import numpy as np

# УГЛОВЫЕ КОЭФФИЦИЕНТЫ
def elementary(center_i: np.ndarray, center_j: np.ndarray, normal_i: np.ndarray, normal_j: np.ndarray, F_j):
    # F_j - площадь одной ячейки коллектора.
    r_vector = center_j - center_i
    r = np.linalg.norm(r_vector)
    n_i, n_j = np.linalg.norm(normal_i), np.linalg.norm(normal_j)

    cos_i = abs( np.dot(normal_i, r_vector) ) / (r * n_i)
    cos_j = abs( np.dot(normal_j, r_vector) ) / (r * n_j)
    return cos_i * cos_j / (np.pi * r ** 2) * F_j


def emitter_to_collector(centers_i, centers_j, normal_i, normal_j, F_i, F_j):
    def local(center_i, centers_j, normal_i, normal_j, F_j):
        return sum([elementary(center_i, center, normal_i, normal_j, F_j) for center in centers_j])

    # F_i - площадь одной ячейки эмиттера.
    return sum([local(center, centers_j, normal_i, normal_j, F_j) for center in centers_i]) * F_i


# ПРЯМОУГОЛЬНЫЙ КАНАЛ
class Tube:
    def __init__(self, a, b, L, cell=0.01):
        self.a = a
        self.b = b
        self.L = L
        self.cell = cell
        self.areas = [a * b, a * b, a * L, b * L, a * L, b * L]
        self.breaks = [self.breaking(i) for i in range(1, 7)]
        self.normals = [[0, 1, 0], [0, -1, 0], [0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0]]

    def breaking(self, i):
        # РАЗБИЕНИЕ
        # функции разбиения каждой пары поверхностей на ячейки.
        # 1-входное, 2-выходное сечения.
        # 3-верхняя, 5-нижняя грани.
        # если смотреть в направлении от 1 к 2, то
        # 3,4,5 и 6 грани пронумерованы по часовой стрелкеf.
        def br_12(i) -> np.ndarray:
            if i != 1 and i != 2:
                raise ValueError("Unsuitable side number : 1 or 2")
            y = 0.0 if i == 1 else float(self.L)
            step = np.sqrt(self.cell)
            l_1 = int(self.a / step)
            l_2 = int(self.b / step)
            res = np.array([np.array([0.0]*3) for _ in range(l_1*l_2)])
            index = 0
            for i in range(l_1):
                x = step / 2 + step * i
                for j in range(l_2):
                    z = step / 2 + step * j
                    center = np.array([x, y, z])
                    res[index] = center
                    index += 1
            return res

        def br_35(i) -> np.ndarray:
            if i != 3 and i != 5:
                raise ValueError("Unsuitable side number : 3 or 5")
            z = 0.0 if i == 5 else float(self.b)
            step = np.sqrt(self.cell)
            l_1 = int(self.a / step)
            l_2 = int(self.L / step)
            res = np.array([np.array([0.0]*3) for _ in range(l_1*l_2)])
            index = 0
            for i in range(l_1):
                x = step / 2 + step * i
                for j in range(l_2):
                    y = step / 2 + step * j
                    center = np.array([x, y, z])
                    res[index] = center
                    index += 1
            return res

        def br_46(i) -> np.ndarray:
            if i != 4 and i != 6:
                raise ValueError("Unsuitable side number : 4 or 6")
            x = 0.0 if i == 4 else float(self.a)
            step = np.sqrt(self.cell)
            l_1 = int(self.L / step)
            l_2 = int(self.b / step)
            res = np.array([np.array([0.0]*3) for _ in range(l_1*l_2)])
            index = 0
            for i in range(l_1):
                y = step / 2 + step * i
                for j in range(l_2):
                    z = step / 2 + step * j
                    center = np.array([x, y, z])
                    res[index] = center
                    index += 1
            return res

        try:
            if i < 3:
                return br_12(i)
            elif i == 3 or i == 5:
                return br_35(i)
            else:
                return br_46(i)
        except ValueError as err:
            print("ValueError:", err)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def num_of_cells(self, i):
        # i - номер искомого эмиттера
        i -= 1
        return len(self.breaks[i])

    def angular_coeff(self, i, j):
        # i - номер эмиттера   от 1 до 6.
        # j - номер коллектора от 1 до 6.
        # cell - площадь ячейки.
        i -= 1  # это - номер эмиттера   в массивах.
        j -= 1  # это - номер коллектора в массивах.

        # параметры коллектора:
        collectors = self.breaks[j]
        normal_j = self.normals[j]

        # параметры эмиттера:
        emitters = self.breaks[i]
        normal_i = self.normals[i]
        area_i = self.areas[i]
        return emitter_to_collector(emitters, collectors, normal_i, normal_j, self.cell, self.cell) / area_i

    def check_add(self, i, j):
        # i - номер эмиттера   от 1 до 6.
        # j - номер коллектора от 1 до 6.
        # cell - размер ячейки.
        i -= 1  # это - номер эмиттера   в массивах.
        j -= 1  # это - номер коллектора в массивах.

        # параметры коллектора:
        collectors = self.breaks[j]
        normal_j = self.normals[j]

        # параметры эмиттера:
        emitters = self.breaks[i]
        normal_i = self.normals[i]
        area_i = self.areas[i]
        # изменили порядок суммирования
        # по сравнению с self.angular_coeff(i,j)
        return emitter_to_collector(collectors, emitters, normal_j, normal_i, self.cell, self.cell) / area_i

    def matrix(self):
        res = [[0] * 7 for _ in range(7)]  # будущая матрица УК.
        for i in range(1, 7):
            for j in range(1, 7):
                if i != j:
                    res[i][j] = self.angular_coeff(i, j)
        return res


#ПРОВЕРКА И ОТВЕТ
def check_solution(phi, x):
    A = np.array([[1, 0, 0],
         [-phi[1][3], 1 - phi[5][3], -2 * phi[4][3]],
         [-phi[1][4], -2 * phi[3][4], 1 - phi[6][4]]])

    b = np.array([1, 0, 0])
    return np.allclose(np.dot(A, x), b)


def flows(phi):
    # СЛУ
    A = np.array([[1, 0, 0],
                  [-phi[1][3], 1 - phi[5][3], -2 * phi[4][3]],
                  [-phi[1][4], -2 * phi[3][4], 1 - phi[6][4]]])
    b = np.array([1, 0, 0])
    return np.linalg.solve(A, b)


def clausing(phi):
    q = flows(phi)
    return (phi[1][2] * q[0]) + 2 * (phi[3][2] * q[1]) + 2 * (phi[4][2] * q[2])
