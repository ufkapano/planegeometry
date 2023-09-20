#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon

point_list = [Point(random.random(), random.random()) for _ in range(5)]

x = [p.x for p in point_list]
y = [p.y for p in point_list]
x.append(x[0])
y.append(y[0])

plt.plot(x, y, 'k.-')

plt.title("Random polygon")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.show()

# EOF
