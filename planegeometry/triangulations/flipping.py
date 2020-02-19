#!/usr/bin/python

import random
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection
from planegeometry.algorithms.geomtools import orientation


class DelaunayFlipping:
    """Delaunay triangulation (flipping edges)."""

    def __init__(self, point_list):
        self.point_list = point_list
        self.tc = TriangleCollection()
        self.big_nodes = None

    def run(self):
        self.insert_big_triangle()
        random.shuffle(self.point_list)
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
        # Counterclockwise orientation of points.
        self.big_nodes = set([p1, p2, p3])
        self.tc.insert(Triangle(p1, p2, p3))

    def add_to_triangulation(self, point):
        #print ( "add_to_triangulation {}".format(point) )
        # Szukamy trojkata do ktorego wpada punkt.
        # Punkt moze byc na krawedzi, na granicy dwoch trojkatow.
        tlist = self.tc.search(point)
        # tlist moze zawierac jeden lub dwa trojkaty (wspolna krawedz).
        #print ( "tlist {}".format(tlist) )
        if len(tlist) == 1:   # punkt we wnetrzu trojkata
            # UWAGA Punkt moze trafic na krawedz big triangle,
            # a wtedy bedzie degeneracja.
            # Chyba ze zrobimy jeszcze wiekszy big triangle.
            t1 = tlist.pop()
            self.tc.remove(t1)
            self.tc.insert(Triangle(t1.pt1, t1.pt2, point))
            self.tc.insert(Triangle(t1.pt2, t1.pt3, point))
            self.tc.insert(Triangle(t1.pt3, t1.pt1, point))
            self.legalize(point, Segment(t1.pt1, t1.pt2))
            self.legalize(point, Segment(t1.pt2, t1.pt3))
            self.legalize(point, Segment(t1.pt3, t1.pt1))
        elif len(tlist) == 2:   # punkt na krawedzi
            t1 = tlist.pop()
            t2 = tlist.pop()
            # Trzeba znalezc wspolna krawedz.
            segment = t1.common_segment(t2)
            assert point in segment
            # Konce wspolnej krawedzi.
            q1 = segment.pt1
            q2 = segment.pt2
            q3 = t1.third_node(q1, q2)
            q4 = t2.third_node(q1, q2)
            self.tc.remove(t1)
            self.tc.remove(t2)
            self.tc.insert(Triangle(q1, q3, point))
            self.tc.insert(Triangle(q2, q3, point))
            self.tc.insert(Triangle(q1, q4, point))
            self.tc.insert(Triangle(q2, q4, point))
            self.legalize(point, Segment(q1, q3))
            self.legalize(point, Segment(q2, q3))
            self.legalize(point, Segment(q1, q4))
            self.legalize(point, Segment(q2, q4))
        else:
            raise ValueError("more than 2 points in tlist")

    def legalize(self, point, segment):
        #print ( "legalize {} {}".format(point, segment) )
        # Trzeba znalezc trojkaty sasiadujace z krawedzia.
        tlist = self.tc.search(segment.center())
        if len(tlist) == 1:   # przypadek (i) de Berga
            # Nie przekrecamy krawedzi duzego trojkata, jest legalna.
            #print ( "big triangle segment" )
            assert segment.pt1 in self.big_nodes and segment.pt2 in self.big_nodes
            return
        #print ( "tlist {}".format(tlist) )
        assert len(tlist) == 2
        t1 = tlist.pop()
        t2 = tlist.pop()
        if point in t2:   # chcemy point in t1
            t1, t2 = t2, t1
        pt3 = t2.third_node(segment.pt1, segment.pt2)
        illegal = t1.in_circumcircle(pt3)
        if pt3 in self.big_nodes:
            #print ( "{} in big_nodes".format(pt3) )
            # Trzeba sprawdzic, czy koniec krawedzi nie jest z big triangle.
            if segment.pt1 in self.big_nodes: # przypadek (iv) de Berga
                # Dokladnie dwa indeksy sa ujemne, jeden z krawedzi.
                illegal = False if segment.pt1 < pt3 else True
                #print ( "illegal 2 {}".format(illegal) )
            elif segment.pt2 in self.big_nodes: # przypadek (iv) de Berga
                # Dokladnie dwa indeksy sa ujemne, jeden z krawedzi.
                illegal = False if segment.pt2 < pt3 else True
                #print ( "illegal 2 {}".format(illegal) )
            else: # przypadek (iii) de Berga
                # Dokladnie jeden indeks ujemny (pt3), ale nie przy krawedzi.
                illegal = False   # krawedz jest legalna
                #print ( "illegal 1 {}".format(illegal) )
        else: # jeden koniec krawedzi moze byc z big triangle
            if segment.pt1 in self.big_nodes or segment.pt2 in self.big_nodes:
                # Przypadek (iii) de Berga, jeden indeks ujemny z krawedzi.
                illegal = True
                #print ( "illegal 1 {}".format(illegal) )
            else:   # cztery indeksy sa dodatnie, przypadek (ii) de Berga,
                pass # procedujemy normalnie
        if illegal:
            if orientation(point, segment.pt1, pt3) * orientation(point, segment.pt2, pt3) > 0:
                # Czworokat wklesly! Nie przekrecamy!
                #print ( "concave quadrilateral!" )
                illegal = False
        if illegal:   # jezeli krawedz nielegalna
            # Przekrecamy krawedz (edge flipping).
            #print ( "segment flip" )
            self.tc.remove(t1)
            self.tc.remove(t2)
            self.tc.insert(Triangle(segment.pt1, point, pt3))
            self.tc.insert(Triangle(segment.pt2, point, pt3))
            self.legalize(point, Segment(segment.pt1, pt3))
            self.legalize(point, Segment(segment.pt2, pt3))

    def remove_big_triangle(self):
        #print ( "remove_big_triangle ..." )
        for point in self.big_nodes:
            for triangle in self.tc.search(point):
                self.tc.remove(triangle)

# EOF
