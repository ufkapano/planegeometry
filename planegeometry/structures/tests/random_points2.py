#!/usr/bin/python

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point

point_list = []
for i in range(100):
    point_list.append(Point(random.random(), random.random()))

x = [p.x for p in point_list]
y = [p.y for p in point_list]
plt.plot(x, y, marker='.', linestyle='None')
# https://matplotlib.org/3.1.1/api/markers_api.html
# matplotlib.markers:
# "D'  diamond
# "."  point
# "o"  circle
# "s"  square

plt.title("Random points")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# EOF
