#!/usr/bin/env python3
#
# Rzucamy odcinkami o jednakowej dlugosci, jak zapalkami.

import random
import math
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

box_size = 5
length = 1.0

plt.axis([0, box_size, 0, box_size])
#plt.axis("equal")   # nie dziala, inne tez
plt.title("Unit segments")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.grid(color='grey')

for i in range(20):
    x1 = random.random() * box_size
    y1 = random.random() * box_size
    angle = 2 * math.pi * random.random()
    x2 = x1 + length * math.cos(angle)
    y2 = y1 + length * math.sin(angle)
    if x2 < 0:
        x1 += length
        x2 += length
    if x2 > box_size:
        x1 -= length
        x2 -= length
    if y2 < 0:
        y1 += length
        y2 += length
    if y2 > box_size:
        y1 -= length
        y2 -= length
    #segment = Segment(x1, y1, x2, y2)
    #x = [segment.pt1.x, segment.pt2.x]
    #y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'ko-')
    #plt.plot(x, y, 'k.-')
    plt.plot([x1, x2], [y1, y2], 'k.-')

plt.show()

# EOF
