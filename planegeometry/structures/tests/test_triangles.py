#!/usr/bin/python

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle

class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.t1 = Triangle(0, 0, 6, 0, 0, 12)
        self.t2 = Triangle(3, 0, 9, 0, 6, 6)
        self.t3 = Triangle(Point(0, 0), Point(2, 0), Point(1, 2))
        self.t4 = Triangle(Fraction(1, 2), Fraction(2, 3), Fraction(3, 4),
            Fraction(4, 5), Fraction(5, 6), Fraction(6, 7))

    def test_init(self):
        self.assertRaises(ValueError, Triangle, 0, 0, 1, 1, 3, 3)
        self.assertRaises(ValueError, Triangle, 0, 0, 1, 1, 3)
        self.assertRaises(ValueError, Triangle, 0, 0, 1, 1)
        self.assertRaises(ValueError, Triangle, Point(1, 1), Point(2, 2), 3)
        self.assertEqual(self.t1.pt1, Point(0, 0))
        self.assertEqual(self.t1.pt2, Point(6, 0))
        self.assertEqual(self.t1.pt3, Point(0, 12))
        self.assertEqual(self.t3.pt1, Point(0, 0))
        self.assertEqual(self.t3.pt2, Point(2, 0))
        self.assertEqual(self.t3.pt3, Point(1, 2))

    def test_print(self):
        self.assertEqual(repr(self.t1), "Triangle(0, 0, 6, 0, 0, 12)")
        self.assertEqual(repr(self.t2), "Triangle(3, 0, 9, 0, 6, 6)")
        self.assertEqual(repr(self.t3), "Triangle(0, 0, 2, 0, 1, 2)")
        self.assertEqual(repr(self.t4), 
        "Triangle(Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(5, 6), Fraction(6, 7))")

    def test_cmp(self):
        self.assertEqual(Triangle(), Triangle(0, 0, 1, 0, 0, 1))
        self.assertTrue(self.t1 == Triangle(0, 0, 6, 0, 0, 12))
        self.assertFalse(self.t1 == self.t2)
        self.assertTrue(self.t1 != self.t2)
        self.assertFalse(self.t1 != Triangle(0, 0, 6, 0, 0, 12))

    def test_copy(self):
        t3 = self.t1.copy()
        self.assertEqual(t3, self.t1)
        self.assertNotEqual(id(t3), id(self.t1))

    def test_center(self):
        self.assertEqual(self.t1.center(), Point(2, 4))
        self.assertEqual(self.t2.center(), Point(6, 2))

    def test_area(self):
        self.assertEqual(self.t1.area(), 36)
        self.assertEqual(self.t2.area(), 18)

    def test_move(self):
        self.assertEqual(self.t1.move(1, 2), Triangle(1, 2, 7, 2, 1, 14))
        self.assertEqual(self.t1.move(Point(1, 2)), Triangle(1, 2, 7, 2, 1, 14))
        self.assertRaises(ValueError, Triangle.move, self.t1, 1)

    def test_make3(self):
        t1 = Triangle(0, 0, 6, 0, 2, 4)
        t2 = Triangle(6, 0, 0, 12, 2, 4)
        t3 = Triangle(0, 12, 0, 0, 2, 4)
        result = self.t1.make3()
        self.assertTrue(t1 in result)
        self.assertTrue(t2 in result)
        self.assertTrue(t3 in result)

    def test_make4(self):
        t1 = Triangle(0, 0, 3, 0, 0, 6)
        t2 = Triangle(6, 0, 3, 6, 3, 0)
        t3 = Triangle(0, 12, 0, 6, 3, 6)
        t4 = Triangle(3, 0, 3, 6, 0, 6)
        result = self.t1.make4()
        self.assertTrue(t1 in result)
        self.assertTrue(t2 in result)
        self.assertTrue(t3 in result)
        self.assertTrue(t4 in result)

    def test_hash(self):
        aset = set()
        aset.add(self.t1)
        aset.add(self.t1)   # ignored
        self.assertEqual(len(aset), 1)
        aset.add(self.t2)
        self.assertEqual(len(aset), 2)

    def test_contains(self):
        self.assertTrue(Point(2, 2) in self.t1)
        self.assertTrue(Point(4, 4) in self.t1)
        self.assertTrue(Point(3, 0) in self.t1)
        self.assertTrue(Point(0, 8) in self.t1)
        self.assertFalse(Point(6, 6) in self.t1)
        self.assertFalse(Point(7, 0) in self.t1)
        self.assertFalse(Point(0, 13) in self.t1)
        self.assertRaises(ValueError, Triangle.__contains__, self.t1, 1)

    def test_orientation(self):
        self.assertEqual(self.t1.orientation(), 1)
        self.assertEqual(Triangle(0, 0, 1, 1, 1, 0).orientation(), -1)

    def test_gnu(self):
        s1 = 'set label "" at 0.0,0.0 point pt 7 ps 0.5\n'
        s2 = 'set label "" at 6.0,0.0 point pt 7 ps 0.5\n'
        s3 = 'set label "" at 0.0,12.0 point pt 7 ps 0.5\n'
        s4 = 'set arrow from 0.0,0.0 to 6.0,0.0 nohead\n'
        s5 = 'set arrow from 0.0,0.0 to 0.0,12.0 nohead\n'
        s6 = 'set arrow from 6.0,0.0 to 0.0,12.0 nohead\n'
        self.assertEqual(self.t1.gnu(True), s1 + s2 + s3 + s4 + s5 + s6)

    def test_third_node(self):
        p1 = Point(0, 0)
        p2 = Point(6, 0)
        p3 = Point(0, 12)
        self.assertEqual(self.t1.third_node(p1, p2), p3)
        self.assertEqual(self.t1.third_node(p1, p3), p2)
        self.assertEqual(self.t1.third_node(p3, p2), p1)
        self.assertRaises(KeyError, Triangle.third_node, self.t1, p1, Point(1, 1))

    def test_in_circumcircle(self):
        # Srodek okregu opisanego na t1 jest w Point(3, 6).
        self.assertTrue(self.t1.in_circumcircle(Point(1, 1)))
        self.assertTrue(self.t1.in_circumcircle(Point(6, 11)))
        self.assertFalse(self.t1.in_circumcircle(Point(7, 0)))

        self.t1 = Triangle(0, 0, 6, 0, 0, 12)

    def test_itersegments(self):
        L = list(self.t1.itersegments())
        self.assertTrue(Segment(0, 0, 6, 0) in L)
        self.assertTrue(Segment(0, 0, 0, 12) in L)
        self.assertTrue(Segment(0, 12, 6, 0) in L)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()     # wlacza wszystkie testy

# EOF
