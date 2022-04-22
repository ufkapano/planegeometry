#!/usr/bin/env python3

import unittest
import math
import random
from planegeometry.structures.points import Point
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.quadtree import QuadTree

class TestQuadTree(unittest.TestCase):

    def setUp(self):
        self.qt1 = QuadTree(Rectangle(0, 0, 1, 1), 4)

    def test_init(self):
        self.assertEqual(str(self.qt1), "QuadTree(Rectangle(0, 0, 1, 1), 4)")

    def test_insert(self):
        self.assertEqual(len(self.qt1.point_list), 0)
        self.qt1.insert(Point(0.1, 0.1))
        self.assertEqual(len(self.qt1.point_list), 1)
        self.qt1.insert(Point(0.2, 0.2))
        #print self.qt1.point_list
        self.assertEqual(len(self.qt1.point_list), 2)
        self.qt1.insert(Point(0.2, 0.1))
        self.assertEqual(len(self.qt1.point_list), 3)
        self.qt1.insert(Point(0.1, 0.2))
        self.assertEqual(len(self.qt1.point_list), 4)
        self.assertEqual(self.qt1.height(), 1)
        # Teraz bedzie subdivide.
        self.qt1.insert(Point(0.9, 0.9))
        self.assertEqual(len(self.qt1.point_list), 4)
        self.assertEqual(self.qt1.height(), 2)
        #print self.qt1.top_right.point_list
        self.assertEqual(len(self.qt1.top_left.point_list), 0)
        self.assertEqual(len(self.qt1.top_right.point_list), 1)
        self.assertEqual(len(self.qt1.bottom_left.point_list), 0)
        self.assertEqual(len(self.qt1.bottom_right.point_list), 0)
        self.qt1.insert(Point(0.3, 0.8))
        self.assertEqual(len(self.qt1.top_left.point_list), 1)

    def test_query(self):
        p1 = Point(0.4, 0.4)
        p2 = Point(0.6, 0.6)
        self.qt1.insert(p1)
        self.qt1.insert(p2)
        result = self.qt1.query(Rectangle(0.0, 0.0, 0.2, 0.2))
        self.assertEqual(result, [])
        result = self.qt1.query(Rectangle(0.5, 0.5, 0.9, 0.9))
        self.assertEqual(result, [p2])
        result = self.qt1.query(Rectangle(0.3, 0.3, 0.7, 0.7))
        self.assertEqual(result, [p1, p2])
        result = self.qt1.query(Rectangle(1.0, 1.0, 2.0, 2.0))
        self.assertEqual(result, [])

    def test_nearest(self):
        p1 = Point(0.1, 0.1)
        p2 = Point(0.2, 0.2)
        p3 = Point(0.3, 0.3)
        p4 = Point(0.4, 0.4)
        p5 = Point(0.5, 0.5)
        p6 = Point(0.6, 0.6)
        for pt in (p1, p2, p3, p4, p5, p6):
            self.qt1.insert(pt)
        result = self.qt1.nearest(Point(0.7, 0.7))
        self.assertEqual(result, p6)
        result = self.qt1.nearest(Point(0.31, 0.31))
        self.assertEqual(result, p3)
        result = self.qt1.nearest(Point(0.36, 0.36))
        self.assertEqual(result, p4)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
