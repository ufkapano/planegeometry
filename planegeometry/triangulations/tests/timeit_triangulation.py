#!/usr/bin/env python3
#
# Testowanie zlozonosci obliczeniowej triangulacji.
# Nie moze byc wypisywania komunikatow na ekran, bo to spowalnia.

import random
import timeit
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
#from planegeometry.triangulations.fantc import FanTriangulationTC as Triangulation
#from planegeometry.triangulations.fanpm import FanTriangulationPM as Triangulation
#from planegeometry.triangulations.ymonotonetc import YMonotoneTriangulationTC as Triangulation
from planegeometry.triangulations.ymonotonepm import YMonotoneTriangulationPM as Triangulation

point_list = []
# wielokat wypukly z degeneracja, y-monotoniczny
# orientacja wielokata anticlockwise
n = 100
n1 = n // 2
n2 = n - n1
# Dla n nieparzystego mamy n1 < n2.

for i in range(n2):
    point_list.append(Point(1, i))
for i in range(n1):
    point_list.append(Point(0, n2-i))

polygon = Polygon(*point_list)

print ( "Testing Triangulation ..." )
t1 = timeit.Timer(lambda: Triangulation(polygon).run())

# Oddzielam tworzenie mapy od testu - roznica jest niewielka.
#algorithm = Triangulation(polygon)
#t1 = timeit.Timer(lambda: algorithm.run())

print ( "{} {}".format(n, t1.timeit(1)) )   # pojedyncze wykonanie

# EOF
