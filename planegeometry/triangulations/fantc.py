#!/usr/bin/env python3
#
# Triangulacja wachlarzowa.
# Punkty moga byc wspolliniowe.
# Trojkaty zapisane w TriangleCollection.

try:
    range = xrange
except NameError:   # Python 3
    pass

from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection
from planegeometry.algorithms.geomtools import orientation


class FanTriangulation:
    """Fan triangulation of a simple polygon in O(n) time."""

    def __init__(self, polygon):
        if polygon.orientation(test_is_simple=False) < 0:
            raise ValueError("clockwise orientation detected")
        self.point_list = polygon.point_list   # nie ma kopiowania punktow
        self.n = len(self.point_list)
        self.tc = TriangleCollection()

    def run(self):
        # Jezeli jest tylko jeden trojkat.
        if self.n == 3:
            t = Triangle(*self.point_list)
            self.tc.insert(t)
            return
        # Przypadek patologiczny to trojkat z dodanymi punktami na jednym boku.
        # Wtedy sa 3 zakrety pod rzad i wachlarz powinien wychodzic
        # z drugiego zakretu.
        # Rozwiazanie:
        # Zaczne szukac ia od wierzcholka ic, w ktorym nie ma zakretu!
        ic = 0
        # Jak wszedzie beda zakrety, to ic zostanie 0.
        for i in range(self.n):
            if orientation(self.point_list[i],
                           self.point_list[(i+1) % self.n],
                           self.point_list[(i+2) % self.n]) == 0:
                ic = (i+1) % self.n   # nie ma zakretu
                break
        #print ( "ic = {}".format(ic) )
        # Szukam pierwszeo zakretu.
        # Zakladam dodatnia orientacje wielokata (counterclockwise).
        # Przy braku zakretu ia nie bedzie zdefiniowane (wyjatek).
        for i in range(self.n):
            j = (ic + i) % self.n
            if orientation(self.point_list[j],
                           self.point_list[(j+1) % self.n],
                           self.point_list[(j+2) % self.n]) > 0:
                ia = j   # punkt przed pierwszym zakretem
                #print ( "ia = {}".format(ia) )
                break
        # W kazdym wielokacie wypuklym sa co najmniej 3 zakrety.
        # Szukam drugiego zakretu.
        for i in range(self.n):
            j = (ia + 1 + i) % self.n   # zaczynamy od pierwszego zakretu
            k = (ia + 2 + i) % self.n   # za pierwszym zakretem
            if orientation(self.point_list[k],
                           self.point_list[(k+1) % self.n],
                           self.point_list[(k+2) % self.n]) > 0:
                ib = k   # punkt przed drugim zakretem
                #print ( "ib = {}".format(ib) )
                # Odcinam trojkat dochodzacy do ib.
                t = Triangle(self.point_list[ia],
                             self.point_list[j],
                             self.point_list[k])
                self.tc.insert(t)
                #print ( t )
                break
            else:   # trzeba odciac trojkat
                t = Triangle(self.point_list[ia],
                             self.point_list[j],
                             self.point_list[k])
                self.tc.insert(t)
                #print ( t )
        # Etap III. Wlasciwa triangulacja wachlarzowa.
        for i in range(self.n):
            j = (ib + 1 + i) % self.n   # zaczynamy od drugiego zakretu
            k = (ib + 2 + i) % self.n   # nastepny
            t = Triangle(self.point_list[ib],
                         self.point_list[j],
                         self.point_list[k])
            self.tc.insert(t)
            #print ( t )
            if k == ia:   # to byl ostatni trojkat
                break

# EOF
