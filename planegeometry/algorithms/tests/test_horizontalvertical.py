#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.horizontalvertical import HorizontalVertical

# 10      o
# 9   o   |
# 8   |   | o-------o
# 7 o-+---+---o
# 6   |   |       o
# 5   | o-+-------+----o
# 4   |   |     o |
# 3   |   o     | |
# 2   |         o |
# 1   o           |
# 0               o
#   0 1 2 3 4 5 6 7 8 9

class TestHorizontalVertical(unittest.TestCase):

    def setUp(self):
        self.segments1 = []
        # vertical
        self.segments1.append(Segment(1, 1, 1, 9))
        self.segments1.append(Segment(3, 3, 3, 10))
        self.segments1.append(Segment(6, 2, 6, 4))
        self.segments1.append(Segment(7, 0, 7, 6))
        # horizontal
        self.segments1.append(Segment(2, 5, 9, 5))
        self.segments1.append(Segment(0, 7, 5, 7))
        self.segments1.append(Segment(4, 8, 8, 8))
        # intersections
        self.points1 = [Point(1, 7), Point(3, 5), Point(3, 7), Point(7, 5)]

    def test_run(self):
        algorithm = HorizontalVertical(self.segments1)
        algorithm.run()
        self.assertEqual(sorted(algorithm.il), sorted(self.points1))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
