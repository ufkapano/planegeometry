#!/usr/bin/python3

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.hulls.jarvis import JarvisMarch

#     x
# x o   x
# x o o
# . x

class TestJarvis1(unittest.TestCase):

    def setUp(self):
        self.point_list = [Point(1, 0), Point(0, 1), Point(1, 1),
            Point(2, 1), Point(0, 2), Point(1, 2), Point(3, 2), 
            Point(2, 3), Point(Fraction(1, 2), Fraction(1, 2))]
        self.convex_hull = [Point(1, 0), Point(3, 2), Point(2, 3), 
            Point(0, 2), Point(0, 1)]

    def test_jarvis(self):
        algorithm = JarvisMarch(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.convex_hull, self.convex_hull)

    def tearDown(self): pass

#         x patologia
#       o
#     o
# . x

class TestJarvis2(unittest.TestCase):

    def setUp(self):
        self.point_list = [Point(1, 0), Point(4, 3), Point(3, 2), Point(2, 1)]
        self.convex_hull = [Point(1, 0), Point(4, 3)]

    def test_jarvis(self):
        algorithm = JarvisMarch(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.convex_hull, self.convex_hull)

    def tearDown(self): pass

# x o o x   s = 4
# o o o o
# o o o o
# x o o x

class TestJarvis3(unittest.TestCase):

    def setUp(self):
        s = 5
        self.point_list = [Point(i, j) for i in range(s) for j in range(s)]
        self.convex_hull = [Point(0, 0), Point(s-1, 0), Point(s-1, s-1), Point(0, s-1)]

    def test_jarvis(self):
        algorithm = JarvisMarch(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.convex_hull, self.convex_hull)

    def tearDown(self): pass

# x       x
#   o   o
# .   x

class TestJarvis4(unittest.TestCase):

    def setUp(self):
        self.point_list = [Point(1, 1), Point(2, 0), Point(3, 1),
            Point(0, 2), Point(4, 2)]
        self.convex_hull = [Point(2, 0), Point(4, 2), Point(0, 2)]

    def test_jarvis(self):
        algorithm = JarvisMarch(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.convex_hull, self.convex_hull)

    def tearDown(self): pass

#   x o x      s = 5
# x o o o x
# o o o o o
# x o o o x
#   x o x

class TestJarvis5(unittest.TestCase):

    def setUp(self):
        s = 5
        assert s > 3
        self.point_list = []
        A = set([0, s-1])
        for i in range(s):
            for j in range(s):
                if (i in A) and (j in A): # odrzucamy narozniki
                    continue
                self.point_list.append(Point(i, j))
        self.convex_hull = [
            Point(1, 0), Point(s-2, 0), Point(s-1, 1), Point(s-1, s-2),
            Point(s-2, s-1), Point(1, s-1), Point(0, s-2), Point(0, 1)]

    def test_jarvis(self):
        algorithm = JarvisMarch(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.convex_hull, self.convex_hull)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
