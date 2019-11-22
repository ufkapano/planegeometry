#!/usr/bin/python

import random
import subprocess
from planegeometry.structures.points import Point

proc = subprocess.Popen(['gnuplot', '--persist'],
    shell=False,
    stdin=subprocess.PIPE,
    )

for i in range(100):
    point = Point(random.random(), random.random())
    #proc.stdin.write(bytearray(point.gnu(), encoqding='utf-8'))
    proc.stdin.write(bytearray(point.gnu(), encoding='ascii'))

proc.stdin.write(b'set terminal pdf enhanced \n')
proc.stdin.write(b'set output "random_points3.pdf" \n')
proc.stdin.write(b'set grid \n')
proc.stdin.write(b'unset key \n')
proc.stdin.write(b'set size square \n')
proc.stdin.write(b'set xlabel "x" \n')
proc.stdin.write(b'set xlabel "y" \n')
proc.stdin.write(b'set title "Random points" \n')
proc.stdin.write(b'set xrange [0:1] \n')
proc.stdin.write(b'set yrange [0:1] \n')
proc.stdin.write(b'plot NaN title "" \n')
proc.stdin.write(b'unset output \n')
proc.stdin.write(b'quit \n')

# EOF
