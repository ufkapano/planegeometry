#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.edges import Edge
from planegeometry.structures.planarmaps import PlanarMap

# A --- B
# |  /  |
# | /   |
# C     D

class TestPlanarMap(unittest.TestCase):

    def setUp(self):
        self.M = PlanarMap()
        A, B, C, D = Point(0, 1), Point(1, 1), Point(0, 0), Point(1, 0)
        self.M.add_first_edge(Segment(A, B))
        self.M.add_leaf(Segment(A, C))
        self.M.add_leaf(Segment(B, D))
        self.M.add_chord(Segment(C, B))
        #self.G.show()

    def test_add_first_edge(self):
        M1 = PlanarMap()
        A, B, C, D = Point(0, 1), Point(1, 1), Point(0, 0), Point(1, 0)
        # not segment
        self.assertRaises(AssertionError, M1.add_first_edge, Edge(B, D))
        M1.add_first_edge(Segment(A, B))
        # second segment
        self.assertRaises(AssertionError, M1.add_first_edge, Segment(B, D))

    def test_add_leaf(self):
        M1 = PlanarMap()
        A, B, C, D = Point(0, 1), Point(1, 1), Point(0, 0), Point(1, 0)
        # empty map
        self.assertRaises(AssertionError, M1.add_leaf, Segment(B, D))
        M1.add_first_edge(Segment(A, B))
        M1.add_leaf(Segment(A, C))
        # adding chord
        self.assertRaises(AssertionError, M1.add_leaf, Segment(B, C))
        # adding the same leaf
        self.assertRaises(AssertionError, M1.add_leaf, Segment(A, C))
        #M1.show()

    def test_add_chord(self):
        M1 = PlanarMap()
        A, B, C, D = Point(0, 1), Point(1, 1), Point(0, 0), Point(1, 0)
        # empty map
        self.assertRaises(AssertionError, M1.add_chord, Segment(B, D))
        M1.add_first_edge(Segment(A, B))
        # adding leaf
        self.assertRaises(AssertionError, M1.add_chord, Segment(A, C))
        M1.add_leaf(Segment(A, C))
        M1.add_chord(Segment(C, B))
        # adding the same chord
        self.assertRaises(ValueError, M1.add_chord, Segment(A, B))
        #M1.show()

    def test_parameters(self):
        self.assertEqual(self.M.v(), 4)
        self.assertEqual(self.M.e(), 4)
        self.assertEqual(self.M.f(), 2)

    def test_iteredges(self):
        B = Point(1, 1)
        Bout = list(self.M.iteroutedges(B))
        Bin = list(self.M.iterinedges(B))
        self.assertEqual(len(Bout), 3)
        self.assertEqual(len(Bin), 3)
        for segment in self.M.iteroutedges(B):
            self.assertEqual(segment.source, B)
        for segment in self.M.iterinedges(B):
            self.assertEqual(segment.target, B)

    def test_iteredges_connected(self):
        start_edge = next(self.M.iteredges())
        A = set([start_edge.source, start_edge.target])
        for edge in self.M.iteredges_connected(start_edge):
            B = set([edge.source, edge.target])
            self.assertTrue(len(A & B) > 0)
            A.update(B)
            #print ( A )

    def test_copy(self):
        T = self.M.copy()
        self.assertEqual(T.v(), self.M.v())
        self.assertEqual(T.e(), self.M.e())
        for node in T.iternodes():
            self.assertTrue(self.M.has_node(node))
        for edge in T.iteredges():
            self.assertTrue(self.M.has_edge(edge))

    def test_degree(self):
        self.assertEqual(self.M.degree(Point(0, 1)), 2)
        self.assertEqual(self.M.degree(Point(1, 1)), 3)
        self.assertEqual(self.M.degree(Point(0, 0)), 2)
        self.assertEqual(self.M.degree(Point(1, 0)), 1)

    def test_exceptions(self):
        self.assertRaises(AssertionError, self.M.add_edge, Edge(Point(0, 0), Point(1, 0)))
        #self.assertRaises(ValueError, self.M.add_edge, Segment(Point(0, 0), Point(0, 0)))
        self.assertRaises(ValueError, self.M.add_edge, Segment(Point(1, 0), Point(1, 1)))
        self.assertRaises(AssertionError, self.M.add_node, "A")

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
