from decimal import Decimal
from tube import Tube

t = Tube(1, 1, 1, Decimal("0.05"))
sep = t.separator
br = sep._breaks  # special for tests module
coeffs = t.calc_angular_coeffs()
