#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.edges import Edge
from planegeometry.structures.planarmaps import PlanarMap

# A --- B
# |  /  |
# | /   |
# C     D

class TestPlanarMap1(unittest.TestCase):

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

    def test_divide_edge(self):
        M1 = PlanarMap()
        A, B, C, D = Point(0, 2), Point(2, 2), Point(0, 0), Point(2, 0)
        AB = Segment(A, B)
        M1.add_first_edge(AB)
        #M1.divide_edge(AB, Point(1, 2))
        M1.divide_edge(Segment(A, B), Point(1, 2))   # it works
        self.assertEqual(M1.v(), 3)
        self.assertEqual(M1.e(), 2)
        self.assertEqual(M1.f(), 1)
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

    def test_init_segment(self):
        M1 = PlanarMap(Segment(0, 1, 2, 3))
        self.assertEqual(M1.v(), 2)
        self.assertEqual(M1.e(), 1)
        self.assertEqual(M1.f(), 1)

    def test_init_triangle(self):
        M1 = PlanarMap(Triangle(0, 0, 1, 0, 1, 1))
        self.assertEqual(M1.v(), 3)
        self.assertEqual(M1.e(), 3)
        self.assertEqual(M1.f(), 2)

    def test_init_rectangle(self):
        M1 = PlanarMap(Rectangle(0, 0, 1, 2))
        self.assertEqual(M1.v(), 4)
        self.assertEqual(M1.e(), 4)
        self.assertEqual(M1.f(), 2)

#     D
#   /   \
# E       C
# |       |
# A-------B
    def test_init_polygon(self):
        M1 = PlanarMap(Polygon(0, 0, 2, 0, 2, 1, 1, 2, 0, 1))
        self.assertEqual(M1.v(), 5)
        self.assertEqual(M1.e(), 5)
        self.assertEqual(M1.f(), 2)

#     D
#     |
# A---+---B
#     |
#     C
    def test_mapoverlay1(self):
        M1 = PlanarMap(Segment(0, 1, 2, 1))
        M2 = PlanarMap(Segment(1, 0, 1, 2))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 5)
        self.assertEqual(M3.e(), 4)
        self.assertEqual(M3.f(), 1)
        #print(list(M3.iternodes()))
        #print(list(M3.iteredges()))

    def tearDown(self): pass


class TestPlanarMap2(unittest.TestCase):

    def setUp(self): pass

#      B4------B3   dwa punkty przeciecia map,
#      |       |    na koncu 4 faces
# A4---+---A3  |
# |    |   |   |
# |    B1--+---B2
# |        |
# A1-------A2
    def test_mapoverlay1(self):
        M1 = PlanarMap(Rectangle(0, 0, 2, 2))
        M2 = PlanarMap(Rectangle(1, 1, 3, 3))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 10)
        self.assertEqual(M3.e(), 12)
        self.assertEqual(M3.f(), 4)

#      B4--B3       punkt przeciecia i wspolna czesc krawedzi,
#      |   |        na koncu 4 faces
# A4---+---A3
# |    |   |
# |    B1--B2
# |        |
# A1-------A2
    def test_mapoverlay2(self):
        M1 = PlanarMap(Rectangle(0, 0, 2, 2))
        M2 = PlanarMap(Rectangle(1, 1, 2, 3))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 9)
        self.assertEqual(M3.e(), 11)
        self.assertEqual(M3.f(), 4)

#      B4--B3       4 punkty przeciecia,
#      |   |        na koncu 6 faces
# A4---+---+---A3
# |    |   |   |
# A1---+---+---A2
#      |   |
#      B1--B2
    def test_mapoverlay3(self):
        M1 = PlanarMap(Rectangle(0, 1, 3, 2))
        M2 = PlanarMap(Rectangle(1, 0, 2, 3))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 12)
        self.assertEqual(M3.e(), 16)
        self.assertEqual(M3.f(), 6)
        #print(list(M3.iternodes()))
        #print(list(M3.iteredges()))

#       B1       6 punktow przeciecia,
#      / \         na koncu 8 faces
# A3--x---x---A2
#  \ /     \ /
#   x       x
#  / \     / \
# B2--x---x--B3
#      \ /
#       A1
    def test_mapoverlay4(self):
        M1 = PlanarMap(Triangle(3, 0, 6, 6, 0, 6))
        #M1 = PlanarMap(Triangle(3., 0., 6., 6., 0., 6.))
        M2 = PlanarMap(Triangle(3, 8, 0, 2, 6, 2))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 12)
        self.assertEqual(M3.e(), 18)
        self.assertEqual(M3.f(), 8)
        #print(list(M3.iternodes()))
        #print(list(M3.iteredges()))

# A3  B4--B3
# | \ |   |
# |   x   |
# |   | \ |
# |   |   x
# |   |   | \
# |   |   |   A2
# |   |   | /
# |   |   x
# |   | / |
# |   x   |
# | / |   |
# A1  B1--B2
    def test_mapoverlay5(self):
        M1 = PlanarMap(Triangle(0, 0, 3, 1, 0, 2))
        M2 = PlanarMap(Rectangle(1, 0, 2, 2))
        M3 = M1.map_overlay(M2)
        self.assertEqual(M3.v(), 11)
        self.assertEqual(M3.e(), 15)
        self.assertEqual(M3.f(), 6)
        #print(list(M3.iternodes()))
        #print(list(M3.iteredges()))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
