#!/usr/bin/env python3

import random
import numpy as np
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point

# alpha = y/(x+y) = st / (ct+st) for x >= 0 and y >= 0
t = np.linspace(0, np.pi)   # points on a circle
st = np.sin(t)
ct = np.cos(t)
d = np.abs(st) + np.abs(ct)
alpha = np.where(t < np.pi / 2, st / d, 2 - st / d)

plt.plot(t, 2*t/np.pi, label="line")
plt.plot(t, alpha, label="alpha")

plt.title("Point.alpha()")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# EOF
