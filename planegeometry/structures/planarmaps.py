#!/usr/bin/env python3

try:
    range = xrange
except NameError:   # Python 3
    pass

from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.graphs import Graph

class PlanarMap(Graph):
    """The class defining a planar map (an undirected graph)."""

    def __init__(self, item=None, n=0, directed=False):
        """Load up a PlanarMap instance."""
        Graph.__init__(self)
        # Create a planar map from item.
        if isinstance(item, Segment):
            self.add_first_edge(item)
        elif isinstance(item, Triangle):
            s1, s2, s3 = list(item.itersegments())
            self.add_first_edge(s1)
            self.add_leaf(s2)
            self.add_chord(s3)
        elif isinstance(item, Rectangle):
            s1, s2, s3, s4 = list(item.itersegments())
            self.add_first_edge(s1)
            self.add_leaf(s2)
            self.add_leaf(s3)
            self.add_chord(s4)
        elif isinstance(item, Polygon):
            slist = list(item.itersegments())
            n = len(slist)
            self.add_first_edge(slist[0])
            for i in range(1, n-1):
                self.add_leaf(slist[i])
            self.add_chord(slist[-1])
        else:
            pass   # ignored

    def add_node(self, node):
        """Add a node to the planar map."""
        assert isinstance(node, Point)
        if node not in self:
            self[node] = dict()

    def add_edge(self, edge):
        """Add a segment to the planar map (missing nodes are created)."""
        assert isinstance(edge, Segment)
        if edge.source == edge.target:
            raise ValueError("loops are forbidden")
        self.add_node(edge.source)
        self.add_node(edge.target)
        if edge.target in self[edge.source] or edge.source in self[edge.target]:
            raise ValueError("parallel segments are forbidden")
        self[edge.source][edge.target] = edge
        self[edge.target][edge.source] = ~edge

    def show(self):
        """The planar map presentation."""
        L = []
        for source in self.iternodes():
            L.append("{0!r} : ".format(source))
            for edge in self.iteroutedges(source):
                L.append("{0!r} ".format(edge.target))
            L.append("\n")
        print("".join(L))

    def add_first_edge(self, edge):
        """Add a first edge to the planar graph."""
        assert self.v() == 0 and self.e() == 0
        self.edge_next = dict()
        self.edge_prev = dict()
        self.face2edge = dict()
        self.edge2face = dict()
        self.add_edge(edge)
        assert self.degree(edge.source) == 1
        assert self.degree(edge.target) == 1
        rev_edge = ~edge   # save reference
        self._update1(edge)
        self._update1(rev_edge)
        self.face2edge[0] = edge
        self.edge2face[edge] = 0
        self.edge2face[rev_edge] = 0

    def _update1(self, edge):
        """Update structures at a edge.source with the degree 1."""
        assert self.degree(edge.source) == 1
        self.edge_next[edge] = edge
        self.edge_prev[edge] = edge

    def add_leaf(self, edge):
        """Add edge (leaf)."""
        # Chcemy, aby edge.target byl nowym wierzcholkiem.
        if self.has_node(edge.target):
            rev_edge = edge   # save reference
            edge = ~edge
        else:
            rev_edge = ~edge   # save reference
        assert self.has_node(edge.source)
        assert not self.has_node(edge.target)
        # Nie mozemy miec nakladajacych sie krawedzi!
        for edge2 in self.iteroutedges(edge.source):
            assert edge.target not in edge2
            assert edge2.target not in edge
        # Aktualizacja grafu abstrakcyjnego.
        self.add_edge(edge)
        # Aktualizacja grafu planarnego.
        # Trzeba znalezc miejsce przylaczenia nowej krawedzi
        # pomiedzy te wychodzace z edge.source.
        if self.degree(edge.source) == 2:
            #print ( "add_leaf: degree(edge.source) == 2" )
            for edge2 in self.iteroutedges(edge.source):
                if edge2.target != edge.target:
                    break
            self._update1(rev_edge)
            self._update3(edge2, edge, edge2)
            # Aktualizacja scian. Nie powstaje nowa sciana.
            face = self.edge2face[edge2]
            self.edge2face[edge] = face
            self.edge2face[rev_edge] = face
        else:
            #print ( "add_leaf: degree(edge.source) > 2" )
            # Znajdujemy edge4 i edge5 wychodzace z edge.source.
            edge4, edge5 = self._locate(edge)
            self._update1(rev_edge)
            self._update3(edge4, edge, edge5)
            # Aktualizacja scian.
            face = self.edge2face[edge5]   # lub ~edge4
            self.edge2face[edge] = face
            self.edge2face[rev_edge] = face

    def _update3(self, edge1, edge2, edge3):
        """Update structures at a node with the degree greater than 1.
        edge2 is a new edge inserted between edge1 and edge3
        (counterclockwise direction).
        """
        assert self.degree(edge2.source) > 1
        assert edge1.source == edge2.source
        assert edge2.source == edge3.source
        self.edge_next[edge1] = edge2
        self.edge_next[edge2] = edge3
        self.edge_prev[edge3] = edge2
        self.edge_prev[edge2] = edge1

    def _locate(self, edge):
        """Find a place for the edge."""
        # edge juz jest wstawione do grafu.
        L = list(self.iteroutedges(edge.source))
        L.sort(key=lambda e: (e.target - e.source).alpha())
        i = L.index(edge)
        #print ( L )
        d = len(L)
        edge4 = L[(i + d -1) % d]
        edge5 = L[(i + 1) % d]
        return edge4, edge5

    def add_chord(self, edge):
        """Add edge (chord)."""
        assert self.has_node(edge.source)
        assert self.has_node(edge.target)
        # Aktualizacja grafu abstrakcyjnego.
        self.add_edge(edge)
        # Aktualizacja grafu planarnego.
        # Trzeba znalezc miejsce przylaczenia nowej krawedzi
        # pomiedzy te wychodzace z edge.source i edge.target.
        if self.degree(edge.source) == 2:
            #print ( "add_chord: degree(edge.source) == 2" )
            for edge2 in self.iteroutedges(edge.source):
                if edge2.target != edge.target:
                    break
            self._update3(edge2, edge, edge2)
            face1 = self.edge2face[edge2]
        else:
            #print ( "add_chord: degree(edge.source) > 2" )
            # Znajdujemy edge4 i edge5 wychodzace z edge.source.
            edge4, edge5 = self._locate(edge)
            self._update3(edge4, edge, edge5)
            face1 = self.edge2face[edge5]
        if self.degree(edge.target) == 2:
            #print ( "add_chord: degree(edge.target) == 2" )
            for edge3 in self.iteroutedges(edge.target):
                if edge3.target != edge.source:
                    break
            self._update3(edge3, ~edge, edge3)
        else:
            #print ( "add_chord: degree(edge.target) > 2" )
            # Znajdujemy edge4 i edge5 wychodzace z edge.target.
            edge4, edge5 = self._locate(~edge)
            self._update3(edge4, ~edge, edge5)
        # Aktualizacja scian.
        # Jedna sciana bedzie podzielona na dwie.
        # face1 to stary numer, face2 to nowy numer.
        face2 = max(self.face2edge) + 1
        self.edge2face[edge] = face1   # stary numer
        self.face2edge[face1] = edge   # uaktualniam
        self.face2edge[face2] = ~edge   # uaktualniam
        # Trzeba poprawic numer sciany dla krawedzi
        edge1 = ~edge
        while True:
            self.edge2face[edge1] = face2   # nowy numer
            edge1 = self.edge_next[~edge1]
            if edge1 == ~edge:
                break

    def map_overlay(self, other):
        """Both maps should have a common point."""
        #M1 = self
        #M2 = other
        M3 = self.copy()
        M4 = other.copy()

        # Finding edge2 from M2.
        for edge2 in other.iteredges():
            if any(edge2.intersect(edge1) for edge1 in self.iteredges()):
                break

        for edge4 in other.iteredges_connected(edge2):
            stack = []
            for edge3 in M3.iteredges():
                if edge4.intersect(edge3):
                    stack.append(edge3)
            divide_points = set()
            set4 = set([edge4.source, edge4.target])

            while stack:
                edge3 = stack.pop()
                if edge3.parallel(edge4):
                    set3 = set([edge3.source, edge3.target])
                    if len(set3 & set4) == 2:
                        continue
                    elif len(set3 & set4) == 1:
                        if edge3.source == edge4.source:
                            if edge3.target in edge4:
                                divide_points.add(edge3.target)
                            elif edge4.target in edge3:
                                M3.divide_edge(edge3, edge4.target)
                            else:
                                continue
                        elif edge3.source == edge4.target:
                            if edge3.target in edge4:
                                divide_points.add(edge3.target)
                            elif edge4.source in edge3:
                                M3.divide_edge(edge3, edge4.source)
                            else:
                                continue
                        elif edge3.target == edge4.source:
                            if edge3.source in edge4:
                                divide_points.add(edge3.source)
                            elif edge4.target in edge3:
                                M3.divide_edge(edge3, edge4.target)
                            else:
                                continue
                        elif edge3.target == edge4.target:
                            if edge3.source in edge4:
                                divide_points.add(edge3.source)
                            elif edge4.source in edge3:
                                M3.divide_edge(edge3, edge4.source)
                            else:
                                continue
                        else:
                            raise ValueError("impossible")
                    else:
                        if edge3.source in edge4 and edge3.target in edge4:
                            divide_points.add(edge3.source)
                            divide_points.add(edge3.target)
                        elif edge4.source in edge3 and edge4.target in edge3:
                            M3.divide_edge(edge3, edge4.source)
                            edge31, edge32 = M3.iteroutedges(edge4.source)
                            if edge4.target in edge31:
                                M3.divide_edge(edge31, edge4.target)
                            else:
                                M3.divide_edge(edge32, edge4.target)
                        elif edge3.source in edge4 and edge4.source in edge3:
                            divide_points.add(edge3.source)
                            M3.divide_edge(edge3, edge4.source)
                        elif edge3.source in edge4 and edge4.target in edge3:
                            divide_points.add(edge3.source)
                            M3.divide_edge(edge3, edge4.target)
                        elif edge3.target in edge4 and edge4.source in edge3:
                            divide_points.add(edge3.target)
                            M3.divide_edge(edge3, edge4.source)
                        elif edge3.target in edge4 and edge4.target in edge3:
                            divide_points.add(edge3.target)
                            M3.divide_edge(edge3, edge4.target)
                        else:
                            raise ValueError("impossible")
                else:
                    set3 = set([edge3.source, edge3.target])
                    if len(set3 & set4) == 1:
                        continue
                    if edge3.source in edge4:
                        divide_points.add(edge3.source)
                    elif edge3.target in edge4:
                        divide_points.add(edge3.target)
                    elif edge4.source in edge3:
                        M3.divide_edge(edge3, edge4.source)
                    elif edge4.target in edge3:
                        M3.divide_edge(edge3, edge4.target)
                    else:
                        point = edge3.intersection_point(edge4)
                        M3.divide_edge(edge3, point)
                        divide_points.add(point)

            edge_set = set([edge4])
            while divide_points:  # do wyczerpania punktow podzialu
                point = divide_points.pop()
                for edge in edge_set:  # jedna z krawedzi zawiera punkt
                    if point in edge:
                        M4.divide_edge(edge, point)
                        edge_set.remove(edge)
                        edge_set.update(M4.iteroutedges(point))  # nowe mniejsze krawedzie
                        break

            # Nakladanie podzielonej krawedzi edge4.
            for edge in edge_set:
                if M3.has_edge(edge):
                    continue
                elif M3.has_node(edge.source) and M3.has_node(edge.target):
                    M3.add_chord(edge)
                elif M3.has_node(edge.source) or M3.has_node(edge.target):
                    M3.add_leaf(edge)
                else:
                    raise ValueError("impossible")
        return M3

    def divide_edge(self, edge, node):
        """Divide edge at node."""
        assert node in edge   # for segment only
        assert self.has_edge(edge)
        edge18 = Segment(edge.source, node)
        edge28 = Segment(edge.target, node)
        # Aktualizacja scian. Czasem face1 == face2.
        # Liczba scian sie nie zmieni.
        face1 = self.edge2face[edge]
        face2 = self.edge2face[~edge]
        self.edge2face[edge18] = face1
        self.edge2face[~edge28] = face1
        self.edge2face[edge28] = face2
        self.edge2face[~edge18] = face2
        self.face2edge[face1] = edge18
        self.face2edge[face2] = edge28
        # Aktualizacja grafu abstrakcyjnego.
        self.del_edge(edge)
        self.add_edge(edge18)
        self.add_edge(edge28)
        if self.degree(edge.source) == 1 and self.degree(edge.target) == 1:
            #print ( "case: single edge divided" )
            # face2edge[0] bedzie zawieralo edge lub ~edge, trzeba naprawic.
            # Aktualizacja grafu planarnego.
            self._update_del(edge)
            self._update1(edge18)
            self._update1(edge28)
            self._update3(~edge28, ~edge18, ~edge28)
        elif self.degree(edge.target) == 1:
            #print ( "case: degree(edge.target) == 1" )
            edge13 = self.edge_next[edge]
            edge14 = self.edge_prev[edge]
            # Aktualizacja grafu planarnego.
            self._update_del(edge)
            self._update1(edge28)
            self._update3(~edge28, ~edge18, ~edge28)
            self._update3(edge14, edge18, edge13)
        elif self.degree(edge.source) == 1:
            #print ( "case: degree(edge.source) == 1" )
            edge25 = self.edge_next[~edge]
            edge26 = self.edge_prev[~edge]
            # Aktualizacja grafu planarnego.
            self._update_del(edge)
            self._update1(edge18)
            self._update3(~edge28, ~edge18, ~edge28)
            self._update3(edge26, edge28, edge25)
        else:
            #print ( "case: both ends connected" )
            edge13 = self.edge_next[edge]
            edge14 = self.edge_prev[edge]
            edge25 = self.edge_next[~edge]
            edge26 = self.edge_prev[~edge]
            # Aktualizacja grafu planarnego.
            self._update_del(edge)
            self._update3(~edge28, ~edge18, ~edge28)
            self._update3(edge14, edge18, edge13)
            self._update3(edge26, edge28, edge25)

    def _update_del(self, edge):
        """Update structures for the edge."""
        del self.edge_next[edge]
        del self.edge_next[~edge]
        del self.edge_prev[edge]
        del self.edge_prev[~edge]
        del self.edge2face[edge]
        del self.edge2face[~edge]

# EOF
