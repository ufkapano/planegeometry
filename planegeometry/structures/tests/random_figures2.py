#!/usr/bin/python

import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.circles import Circle

rectangle = Rectangle(0.1, 0.3, 0.9, 0.7)
triangle = Triangle(0.2, 0.2, 0.8, 0.4, 0.6, 0.8)

for segment in rectangle.itersegments():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'bo-')
    plt.plot(x, y, 'b.-')

for segment in triangle.itersegments():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'ro-')
    plt.plot(x, y, 'r.-')

#circle = Circle(0.4, 0.6, 0.2)
# A Circle is a subclass of an Artist.
circle = mpatches.Circle((0.4, 0.6), 0.2, color='g', fill=False)
#plt.gcf().gca().add_artist(circle)
plt.gca().add_artist(circle)

plt.title("Random figures")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# EOF
