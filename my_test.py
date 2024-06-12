from scipy.interpolate import BarycentricInterpolator as Interpolator
from scipy.optimize import fsolve
import numpy as np

x = np.linspace(-100, 100, 1000)
y = x**2 - 16.0
func = Interpolator(x, y)
print(fsolve(func, np.array([0.0]))[0])
