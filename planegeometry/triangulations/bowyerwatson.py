#!/usr/bin/python

import random
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection
from planegeometry.algorithms.geomtools import orientation


class BowyerWatson:
    """Bowyer-Watson algorithm for Delaunay triangulation.
    
    https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    """

    def __init__(self, point_list):
        self.point_list = point_list
        self.tc = TriangleCollection()
        self.big_nodes = None   # chyba lepiej pamietac

    def run(self):
        self.insert_big_triangle()
        # Mozna chwilowo wylaczyc losowanie.
        random.shuffle(self.point_list)   # losowa kolejnosc punktow
        for point in self.point_list:
            self.add_to_triangulation(point)
        self.remove_big_triangle()

    def insert_big_triangle(self):
        big = max(max(abs(point.x), abs(point.y)) for point in self.point_list)
        m = 4   # najlepiej typu int
        # m = 3 sugeruje de Berg, ale moze byc na styk, jezeli beda punkty
        # Point(big, -big) lub Point(-big, big).
        p1 = Point(m * big, 0)
        p2 = Point(0, m * big)
        p3 = Point(-m * big, -m * big)
        # Counterclockwise orientation of points (nieistotne).
        self.big_nodes = set([p1, p2, p3])
        self.tc.insert(Triangle(p1, p2, p3))

    def add_to_triangulation(self, point):
        #print ( "add_to_triangulation {}".format(point) )
        bad_triangles = list()
        for triangle in self.tc.itertriangles():
            if triangle.in_circumcircle(point):
                bad_triangles.append(triangle)
        sdict = dict()
        for triangle in bad_triangles:
            # Sprawdzanie krawedzi.
            for segment in triangle.itersegments():
                sdict[segment] = sdict.get(segment, 0) + 1
        for triangle in bad_triangles:
            self.tc.remove(triangle)
        for segment in sdict:
            if sdict[segment] == 1:
                self.tc.insert(Triangle(point, segment.pt1, segment.pt2))

    def remove_big_triangle(self):
        #print ( "remove_big_triangle ..." )
        for point in self.big_nodes:
            for triangle in self.tc.search(point):
                self.tc.remove(triangle)

# EOF
