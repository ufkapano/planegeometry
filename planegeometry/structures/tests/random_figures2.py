#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.circles import Circle

plt.axis([0, 1, 0, 1])
ax = plt.gca()

rectangle1 = Rectangle(0.1, 0.3, 0.9, 0.7)
# rectangle1 = plt.Rectangle((0.1, 0.3), 0.8, 0.4, fill=False, color='b')
rectangle2 = plt.Rectangle((0.6, 0.1), 0.2, 0.1, fill=False, color='m')
print(rectangle2)   # Rectangle(xy=(0.6, 0.1), width=0.2, height=0.1, angle=0)

for segment in rectangle1.itersegments():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'bo-')
    plt.plot(x, y, 'b.-')

triangle1 = Triangle(0.2, 0.2, 0.8, 0.4, 0.6, 0.8)

for segment in triangle1.itersegments():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'ro-')
    plt.plot(x, y, 'r.-')

#circle1 = Circle(0.4, 0.6, 0.2)
circle1 = plt.Circle((0.4, 0.6), 0.2, color='g', fill=False)
print(circle1)   # Circle(xy=(0.4, 0.6), radius=0.2)

ax.add_patch(circle1)
ax.add_patch(rectangle2)

plt.title("Random figures")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.show()

# EOF
