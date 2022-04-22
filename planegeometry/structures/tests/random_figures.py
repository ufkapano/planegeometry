#!/usr/bin/env python2

import random
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.circles import Circle

gnu = Gnuplot.Gnuplot (persist = 1)

visible = True

rectangle = Rectangle(0.1, 0.3, 0.9, 0.7)
gnu(rectangle.gnu(visible))

triangle = Triangle(0.2, 0.2, 0.8, 0.4, 0.6, 0.8)
gnu(triangle.gnu(visible))

circle = Circle(0.4, 0.6, 0.2)
gnu(circle.gnu(visible))

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "random_figures.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Random figures"')
gnu('set xrange [{}:{}]'.format(0, 1))
gnu('set yrange [{}:{}]'.format(0, 1))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
