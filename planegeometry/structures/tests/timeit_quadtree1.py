#!/usr/bin/env python3
#
# Porownanie quadtree i metody silowej.
# 1. Powyzej 200~1000 punktow QuadTree.nearest() jest szybsze od
# find_nearest().
# 2. Powyzej 20000 punktow QuadTree.query() bylo szybsze od
# find_in_rectangle() dla powierzchni 0.01 calosci.
# 3. Zaleznosc wysokosci drzewa od n.
# UWAGA U mnie punkty siedza w kazdym wezle.
# n        height
# 10       2
# 100      4
# 1000     6
# 10000    8
# 100000   10
# 1000000   12

import timeit
import random
from planegeometry.structures.points import Point
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.quadtree import QuadTree

N = 100
plist = []
quadtree = QuadTree(Rectangle(0, 0, 1, 1))
for i in range(N):
    pt = Point(random.random(), random.random())
    plist.append(pt)
    quadtree.insert(pt)
point1 = Point(random.random(), random.random())
rectangle1 = Rectangle(0.1, 0.1, 0.2, 0.2)
print ( "height {}".format(quadtree.height()) )


def find_nearest1(point_list, point):
    """Szukanie punktu na liscie najblizszego danemu."""
    return min(point_list, key=lambda pt: (point-pt).length())


def find_nearest2(point_list, point):   # 2 times slower!
    """Szukanie punktu na liscie najblizszego danemu."""
    return min(point_list, key=lambda pt: (point-pt) * (point-pt))


def find_in_rectangle(point_list, query_rect):
    """Szukanie punktow z listy nalezacych do prostokata."""
    result = []
    for pt in point_list:
        if pt in query_rect:
            result.append(pt)
    return result


print ( "find_nearest1() {}".format( find_nearest1(plist, point1) ))
print ( "find_nearest2() {}".format( find_nearest2(plist, point1) ))
print ( "quadtree.nearest() {}".format( quadtree.nearest(point1) ))
print ( "find_in_rectangle() {}".format( len(find_in_rectangle(plist, rectangle1)) ))
print ( "quadtree.query() {}".format( len(quadtree.query(rectangle1)) ))

print ( "Testing find_nearest1() ..." )
t1 = timeit.Timer(lambda: find_nearest1(plist, point1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_nearest2() ..." )
t1 = timeit.Timer(lambda: find_nearest2(plist, point1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing QuadTree.nearest() ..." )
t1 = timeit.Timer(lambda: quadtree.nearest(point1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_in_rectangle() ..." )
t1 = timeit.Timer(lambda: find_in_rectangle(plist, rectangle1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing QuadTree.query() ..." )
t1 = timeit.Timer(lambda: quadtree.query(rectangle1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
