#!/usr/bin/env python3

try:
    range = xrange
except NameError:   # Python 3
    pass


from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.trianglecollections import TriangleCollection
from planegeometry.algorithms.geomtools import orientation


class Chain:
    LEFT = 0
    RIGHT = 1


class YMonotoneTriangulationTC:
    """Triangulation of a strictly y-monotone polygon in O(n) time."""

    def __init__(self, polygon):
        if polygon.orientation(test_is_simple=False) < 0:
            raise ValueError("clockwise orientation detected")
        self.point_list = polygon.point_list   # nie ma kopiowania punktow
        self.n = len(self.point_list)
        self.tc = TriangleCollection()
        self.ulist = []   # for pairs (point, chain)
        self.stack = []   # for pairs (point, chain)

    def run(self):
        self.merge_chains()
        self.stack.append(self.ulist[0])
        self.stack.append(self.ulist[1])
        for i in range(2, self.n-1):
            # Processing self.ulist[i]
            point1, chain1 = self.ulist[i]
            point2, chain2 = self.stack[-1]   # top of the stack
            #print ( "new point {}".format(point1) )
            #print ( "stack {}".format(self.stack) )
            if chain1 != chain2:
                #print ( "chain1 != chain2" )
                # Wchodzac tutaj mozemy miec na stosie wierzcholki z drugiego
                # lancucha, ktore tworza luk wygiety na zewnatrz.
                # Mozna je wszystkie (bez ostatniego) polaczyc z point1.
                while len(self.stack) > 1:
                    point2, chain2 = self.stack.pop()
                    # New diagonal (point1, point2).
                    point3, chain3 = self.stack[-1]
                    triangle = Triangle(point1, point2, point3)
                    #print ( triangle )
                    self.tc.insert(triangle)
                #point2, chain2 = self.stack.pop()
                self.stack.pop()   # tego punktu nie potrzebujemy
                assert len(self.stack) == 0
                # Tutaj najnizsza diagonal laczy dwa najnizsze punkty,
                # dlatego te dwa punkty trzeba dac na stos.
                self.stack.append(self.ulist[i-1])
                self.stack.append(self.ulist[i])
            else:   # the same chain
                #print ( "chain1 == chain2" )
                point2, chain2 = self.stack.pop()
                point3, chain3 = self.stack[-1]
                if chain1 == Chain.LEFT:
                    orient = -1
                else:
                    orient = +1
                while orientation(point1, point2, point3) == orient:
                    triangle = Triangle(point1, point2, point3)
                    #print ( triangle )
                    self.tc.insert(triangle)
                    # point2 jest odciety i nie powraca na stos.
                    # Nowa diagonala to (point1, point3).
                    point2, chain2 = self.stack.pop()
                    if len(self.stack) == 0:
                        break
                    else:
                        point3, chain3 = self.stack[-1]
                self.stack.append((point2, chain2))
                self.stack.append(self.ulist[i])
        assert len(self.stack) >= 2
        #print ( "processing the last point" )
        # Przetwarzanie ostatniego punktu.
        # Uzywam jezyka dodawania trojkatow do triangulacji.
        # Jezeli mowimy o diagonalach, to juz istnieja diagonale
        # (ulist[self.n-1], stack[-1]) i (ulist[self.n-1], stack[0])
        # bo to sa boki wielokata.
        point1, chain1 = self.ulist[self.n-1]
        #print ( "new point {}".format(point1) )
        #print ( "stack {}".format(self.stack) )
        point2, chain2 = self.stack.pop()
        while len(self.stack) > 0:
            point3, chain3 = self.stack.pop()
            triangle = Triangle(point1, point2, point3)
            #print ( triangle )
            self.tc.insert(triangle)
            point2 = point3

    def merge_chains(self):
        """Preparing self.ulist with sorted pairs (point, chain)."""
        # Finding the top point and the bottom point.
        i_max = max(range(self.n), key=lambda i: (self.point_list[i].y))
        i_min = min(range(self.n), key=lambda i: (self.point_list[i].y))
        #print ( "i_max {}".format(i_max) )
        #print ( "i_min {}".format(i_min) )
        # Finding the left chain and the right chain.
        # Jezeli orientacja wielokata jest +1, to od i_max zaczyna sie
        # left chain. Jezeli orientacja jest -1, to bedzie right chain.
        left_chain = []
        right_chain = []
        for i in range(self.n):
            j = (i_max + i) % self.n
            if j == i_min:
                break
            left_chain.append(self.point_list[j])
        for i in range(self.n):
            j = (i_min + i) % self.n
            if j == i_max:
                break
            right_chain.append(self.point_list[j])
        right_chain.reverse()
        # Mozna zmienic nazwy, jezeli orientacja jest -1:
        # left_chain, right_chain = right_chain, left_chain

        # Szybciej byloby zrobic merge lewego i prawego lancucha,
        # ale na razie dla prostoty sortuje wszystko na raz.
        self.ulist.extend((point, Chain.LEFT) for point in left_chain)
        self.ulist.extend((point, Chain.RIGHT) for point in right_chain)
        # y maleje, ale dla rownych y bedzie x rosnaco.
        self.ulist.sort(key=lambda item: (item[0].y, -item[0].x), reverse=True)
        #print ( self.ulist )

# EOF
