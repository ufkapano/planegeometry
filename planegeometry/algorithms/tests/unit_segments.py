#!/usr/bin/python
#
# Rzucamy odcinkami o jednakowej dlugosci, jak zapalkami.

import random
import math
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

gnu = Gnuplot.Gnuplot (persist = 1)

visible = True
box_size = 5
length = 1.0
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
    segment = Segment(x1, y1, x2, y2)
    gnu(segment.gnu(visible))

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "unit_segments.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Unit segments"')
gnu('set xrange [{}:{}]'.format(0, box_size))
gnu('set yrange [{}:{}]'.format(0, box_size))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF