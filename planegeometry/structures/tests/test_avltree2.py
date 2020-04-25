#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.avltree2 import AVLTreeModified


class TestAVL(unittest.TestCase):

    def setUp(self):
        self.t1 = AVLTreeModified()
        self.s1 = Segment(0, 0, 7, 7)
        self.s2 = Segment(1, 5, 5, 1)
        self.s3 = Segment(2, 6, 6, 2)
        # Intersection s1 and s2.
        self.p12 = Point(3, 3)
        # Intersection s1 and s3.
        self.p13 = Point(4, 4)
        for segment in (self.s1, self.s2, self.s3):
            if segment.pt1.x > segment.pt2.x:
                segment = ~segment
            # Left endpoints are now important.
            self.t1.current_x = segment.pt1.x
            self.t1.insert(segment)
        # Events:
        # self.s1.pt1 insert
        # self.s2.pt1 insert
        # self.s3.pt1 insert
        # self.p12 intersection
        # self.p13 intersection
        # self.s2.pt2 delete
        # self.s3.pt2 delete
        # self.s1.pt2 delete

    def test_insert(self):
        self.assertEqual(self.t1.root.value, self.s2)
        self.assertEqual(self.t1.root.left.value, self.s1)
        self.assertEqual(self.t1.root.right.value, self.s3)

    def test_successor_predecessor(self):
        self.assertEqual(self.t1.root.successor(), self.t1.root.right)
        self.assertEqual(self.t1.root.left.successor(), self.t1.root)
        self.assertEqual(self.t1.root.right.successor(), None)
        self.assertEqual(self.t1.root.predecessor(), self.t1.root.left)
        self.assertEqual(self.t1.root.right.predecessor(), self.t1.root)
        self.assertEqual(self.t1.root.left.predecessor(), None)

    def test_min_max(self):
        self.assertEqual(self.t1.root.find_min(), self.t1.root.left)
        self.assertEqual(self.t1.root.find_max(), self.t1.root.right)

    def test_intersections(self):
        self.assertEqual(self.t1.root.value, self.s2)
        # The first intersection point p12.
        self.t1.current_x = self.p12.x
        self.t1.swap(self.s2, self.s1)   # above and below
        self.assertEqual(self.t1.root.value, self.s1)
        self.assertEqual(self.t1.successor(self.s2).value, self.s1)
        self.assertEqual(self.t1.successor(self.s1).value, self.s3)
        self.assertEqual(self.t1.predecessor(self.s3).value, self.s1)
        self.assertEqual(self.t1.predecessor(self.s1).value, self.s2)
        # The second intersection point p13.
        self.t1.current_x = self.p13.x
        self.t1.swap(self.s3, self.s1)   # above and below
        self.assertEqual(self.t1.root.value, self.s3)
        self.assertEqual(self.t1.successor(self.s2).value, self.s3)
        self.assertEqual(self.t1.successor(self.s3).value, self.s1)
        self.assertEqual(self.t1.predecessor(self.s1).value, self.s3)
        self.assertEqual(self.t1.predecessor(self.s3).value, self.s2)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
