#!/usr/bin/env python3

import unittest
from planegeometry.structures.points import Point
from planegeometry.algorithms.closestpair4 import ClosestPairSortXY


class TestClosestPair(unittest.TestCase):

    def setUp(self):
        self.point_list = [Point(2, 8), Point(0, 7), Point(5, 6),
            Point(4, 3), Point(7, 2), Point(6, 1), Point(3, 0)]
        self.result = (Point(6, 1), Point(7, 2))

        self.points1 = list()
        self.points1.append(Point(-19, -10))
        self.points1.append(Point(-16, 2))
        self.points1.append(Point(-12, -3))
        self.points1.append(Point(-10, 10))
        self.points1.append(Point(-9, 5))
        self.points1.append(Point(-5, -5))
        self.points1.append(Point(-4, -9))
        self.points1.append(Point(-3, 9))
        self.points1.append(Point(-2, 5))
        self.points1.append(Point(-1, 7))
        self.points1.append(Point(2, 4))
        self.points1.append(Point(6, 13))
        self.points1.append(Point(4, 15))
        self.points1.append(Point(11, -3))
        self.points1.append(Point(14, 3))
        self.points1.append(Point(27, 10))
        self.points1.append(Point(5, -9))
        self.points1.append(Point(8, -4))
        self.points1.append(Point(3, -4))
        self.points1.append(Point(15, -13))
        self.points1.append(Point(17, -7))
        self.points1.append(Point(25, 6))
        self.points1.append(Point(20, 3))
        self.points1.append(Point(24, -2))

        self.points2 = list()
        self.points2.append(Point(1, 3))
        self.points2.append(Point(4, 3))

        self.points3 = list()
        self.points3.append(Point(1, 3))
        self.points3.append(Point(4, 3))
        self.points3.append(Point(0, 0))

    def test_closest_pair(self):
        algorithm = ClosestPairSortXY(self.point_list)
        algorithm.run()
        self.assertEqual(algorithm.closest_pair, self.result)

        self.assertEqual(sorted(ClosestPairSortXY(self.points1).run()),
            sorted((Point(-2, 5), Point(-1, 7))))
        self.assertEqual(sorted(ClosestPairSortXY(self.points2).run()),
            sorted((Point(1, 3), Point(4, 3))))
        self.assertEqual(sorted(ClosestPairSortXY(self.points3).run()),
            sorted((Point(1, 3), Point(4, 3))))

    def test_exceptions(self):
        self.assertRaises(ValueError, ClosestPairSortXY, [Point(1, 1)])

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
