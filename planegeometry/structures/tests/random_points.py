#!/usr/bin/env python2
#
# Gnuplot under Python
#
# http://gnuplot-py.sourceforge.net/
# Gnuplot.py is a Python package that interfaces to gnuplot.
#
# https://pypi.org/project/PyGnuplot/
# Python Gnuplot wrapper
# pip install PyGnuplot   # Python 2.7 and 3.6
#
# https://pypi.org/project/gnuplotlib/
# Gnuplot-based plotting for numpy
# pip install gnuplotlib

import random
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point

gnu = Gnuplot.Gnuplot (persist = 1)

for i in range(100):
    point = Point(random.random(), random.random())
    gnu(point.gnu())

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "random_points.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Random points"')
gnu('set xrange [{}:{}]'.format(0, 1))
gnu('set yrange [{}:{}]'.format(0, 1))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
