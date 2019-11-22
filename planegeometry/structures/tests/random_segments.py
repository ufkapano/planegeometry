#!/usr/bin/python

import random
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

gnu = Gnuplot.Gnuplot (persist = 1)

visible = True
for i in range(10):
    segment = Segment(random.random(), random.random(),
        random.random(), random.random())
    gnu(segment.gnu(visible))

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "random_segments.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Random segments"')
gnu('set xrange [{}:{}]'.format(0, 1))
gnu('set yrange [{}:{}]'.format(0, 1))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
