#!/usr/bin/env python3

import unittest
from planegeometry.structures.points import Point
from planegeometry.structures.edges import Edge
from planegeometry.structures.triangles import Triangle
from planegeometry.triangulations.flipping import DelaunayFlipping


class TestTriangulation(unittest.TestCase):

    def setUp(self): pass

    def test_triangulation(self):
        p1 = Point(-1, -1)
        p2 = Point(1, -1)
        p3 = Point(2, 1)
        p4 = Point(-1, 1)
        point_list = [p1, p2, p3, p4]
        algorithm = DelaunayFlipping(point_list)
        algorithm.run()
        self.assertEqual(len(algorithm.tc), 2)
        self.assertTrue(Triangle(p1, p2, p4) in algorithm.tc)
        self.assertTrue(Triangle(p2, p3, p4) in algorithm.tc)
        #print ( "tc {}".format(algorithm.tc) )
        G = algorithm.tc.to_graph()
        #G.show()
        self.assertEqual(G.v(), 4)
        self.assertEqual(G.e(), 5)
        self.assertTrue(G.has_edge(Edge(p1, p2)))
        self.assertTrue(G.has_edge(Edge(p1, p4)))
        self.assertTrue(G.has_edge(Edge(p2, p4)))
        self.assertTrue(G.has_edge(Edge(p2, p3)))
        self.assertTrue(G.has_edge(Edge(p3, p4)))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
