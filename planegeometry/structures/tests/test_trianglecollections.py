#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection

class TestTriangleCollection(unittest.TestCase):

    def setUp(self):
        self.t1 = Triangle(0, 0, 2, 0, 0, 2)
        self.t2 = Triangle(2, 0, 2, 2, 0, 2)
        self.tc = TriangleCollection()

    def test_collection(self):
        self.assertEqual(len(self.tc), 0)
        self.tc.insert(self.t1)
        self.assertEqual(len(self.tc), 1)
        self.tc.insert(self.t2)
        self.assertEqual(len(self.tc), 2)
        tlist = self.tc.search(Point(1, 1))
        self.assertEqual(len(tlist), 2)
        G = self.tc.to_graph()
        #G.show()
        self.assertEqual(G.v(), 4)
        self.assertEqual(G.e(), 5)
        nodes = set([Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2)])
        self.assertEqual(set(G.iternodes()), nodes)
        self.tc.remove(self.t1)
        self.assertEqual(len(self.tc), 1)
        self.tc.remove(self.t2)
        self.assertEqual(len(self.tc), 0)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
