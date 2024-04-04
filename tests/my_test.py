import numpy as np
from decimal import Decimal
normals = [[0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0]]
for i in range(6):
    normals[i] = np.array(map(Decimal, normals[i]))

