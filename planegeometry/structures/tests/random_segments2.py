#!/usr/bin/python

import random
import matplotlib.pyplot as plt
from planegeometry.structures.segments import Segment

for i in range(10):
    segment = Segment(random.random(), random.random(),
        random.random(), random.random())
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'ko-')
    plt.plot(x, y, 'k.-')

plt.title("Random segments")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# EOF
