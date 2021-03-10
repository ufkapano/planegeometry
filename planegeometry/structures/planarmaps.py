#!/usr/bin/python

try:
    from Queue import Queue
except ImportError:   # Python 3
    from queue import Queue

import random
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

class PlanarMap(dict):
    """The class defining a planar map (an undirected graph)."""

    def __init__(self):
        """Load up a PlanarMap instance."""
        # Structures defining a topological graph.
        self.edge_next = None
        self.edge_prev = None
        self.face2edge = None
        self.edge2face = None

    def v(self):
        """Return the number of nodes (the graph order)."""
        return len(self)

    def e(self):
        """Return the number of edges in O(V) time."""
        return sum(len(self[node]) for node in self) // 2

    def degree(self, source):
        """Return the degree of the node in the undirected graph."""
        assert isinstance(source, Point)
        return len(self[source])

    def f(self):
        """Return the number of faces."""
        if not self.edge_next:
            raise ValueError("empty planar map")
        return self.e() + 2 - self.v()   # Euler's formula

    def iterfaces(self):
        """Generate all faces on demand."""
        if not self.edge_next:
            raise ValueError("empty planar map")
        used = set()
        for edge in self.edge_next:
            if edge in used:
                continue
            used.add(edge)
            face = [edge]
            edge = self.edge_next[~edge]
            while edge not in used:
                used.add(edge)
                face.append(edge)
                edge = self.edge_next[~edge]
            yield face

    def iterface(self, start_edge):
        """Generate edges from the same face on demand."""
        assert isinstance(start_edge, Segment)
        if not self.edge_next:
            raise ValueError("empty planar map")
        edge = start_edge
        while True:
            yield edge
            edge = self.edge_next[~edge]
            if edge == start_edge:
                break

    def add_node(self, node):
        """Add a node to the planar map."""
        assert isinstance(node, Point)
        if node not in self:
            self[node] = dict()

    def has_node(self, node):
        """Test if a node exists."""
        assert isinstance(node, Point)
        return node in self

    def del_node(self, node):
        """Remove a node from the planar map (with edges)."""
        # The dictionary changes size during iteration.
        assert isinstance(node, Point)
        for edge in list(self.iteroutedges(node)):
            self.del_edge(edge)
        del self[node]

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

    def del_edge(self, edge):
        """Remove an edge from the planar map."""
        assert isinstance(edge, Segment)
        del self[edge.source][edge.target]
        del self[edge.target][edge.source]

    def has_edge(self, edge):
        """Test if an edge exists (the weight is not checked)."""
        assert isinstance(edge, Segment)
        return edge.source in self and edge.target in self[edge.source]

    def weight(self, edge):
        """Return the edge weight or zero."""
        assert isinstance(edge, Segment)
        if edge.source in self and edge.target in self[edge.source]:
            return self[edge.source][edge.target].weight
        else:
            return 0

    def iternodes(self):
        """Generate all nodes from the graph on demand."""
        return iter(self)

    def iteradjacent(self, source):
        """Generate the adjacent nodes from the graph on demand."""
        assert isinstance(source, Point)
        return iter(self[source])

    def iteroutedges(self, source):
        """Generate the outedges from the graph on demand."""
        assert isinstance(source, Point)
        for target in self[source]:
            yield self[source][target]

    def iterinedges(self, source):
        """Generate the inedges from the graph on demand."""
        assert isinstance(source, Point)
        for target in self[source]:
            yield self[target][source]

    def iteredges(self):
        """Generate all edges from the planar map on demand."""
        for source in self.iternodes():
            for target in self[source]:
                if source < target:
                    yield self[source][target]

    itersegments = iteredges

    def iteredges_connected(self, start_edge):
        """Generate all connected edges from the planar map on demand."""
        assert isinstance(start_edge, Segment)
        if not self.has_edge(start_edge):
            raise ValueError("edge not in the planar map")
        if start_edge.source > start_edge.target:
            start_edge = ~start_edge
        # Modified BFS starts from here, before while.
        used = set()   # for yielded edges
        parent = dict()   # for BFS tree
        parent[start_edge.source] = None
        parent[start_edge.target] = start_edge.source
        Q = Queue()
        Q.put(start_edge.source)
        Q.put(start_edge.target)
        used.add(start_edge)
        yield start_edge
        while not Q.empty():   # BFS continued
            source = Q.get()
            for edge in self.iteroutedges(source):
                if edge.target not in parent:
                    parent[edge.target] = source   # before Q.put
                    Q.put(edge.target)
                if edge.source > edge.target:
                    edge = ~edge
                if edge not in used:   # start_edge will be detected
                    used.add(edge)
                    yield edge

    def show(self):
        """The planar map presentation."""
        L = []
        for source in self.iternodes():
            L.append("{} : ".format(source))
            for edge in self.iteroutedges(source):
                if edge.weight == 1:
                    L.append("{} ".format(edge.target))
                else:
                    L.append("{}({}) ".format(edge.target, edge.weight))
            L.append("\n")
        print("".join(L))

    def copy(self):
        """Return the planar map copy."""
        new_map = PlanarMap()
        for node in self.iternodes():
            new_map[node] = dict(self[node])
        # Structures defining a topological graph.
        if self.edge_next:
            new_map.edge_next = dict(self.edge_next)
        if self.edge_prev:
            new_map.edge_prev = dict(self.edge_prev)
        if self.face2edge:
            new_map.face2edge = dict(self.face2edge)
        if self.edge2face:
            new_map.edge2face = dict(self.edge2face)
        return new_map

    def __eq__(self, other):
        """Test if the planar maps are equal."""
        if set(self) != set(other):   # checking nodes
            return False
        for node in self.iternodes():   # comparing neighbors
            if self[node] != other[node]:   # different dicts
                return False
        return True

    def __ne__(self, other):
        """Test if the planar maps are not equal."""
        return not self == other

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
        self._update1(edge)
        self._update1(~edge)
        self.face2edge[0] = edge
        self.edge2face[edge] = 0
        self.edge2face[~edge] = 0

    def _update1(self, edge):
        """Update structures at a edge.source with the degree 1."""
        self.edge_next[edge] = edge
        self.edge_prev[edge] = edge

    def add_leaf(self, edge):
        """Add edge (leaf)."""
        if self.has_node(edge.target):
            edge = ~edge
        assert self.has_node(edge.source)
        assert not self.has_node(edge.target)
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
            self._update1(~edge)
            self._update3(edge2, edge, edge2)
            # Aktualizacja scian. Nie powstaje nowa sciana.
            face = self.edge2face[edge2]
            self.edge2face[edge] = face
            self.edge2face[~edge] = face
        else:
            #print ( "add_leaf: degree(edge.source) > 2" )
            # Znajdujemy edge4 i edge5 wychodzace z edge.source.
            edge4, edge5 = self._locate(edge)
            self._update1(~edge)
            self._update3(edge4, edge, edge5)
            # Aktualizacja scian.
            face = self.edge2face[edge5]   # lub ~edge4
            self.edge2face[edge] = face
            self.edge2face[~edge] = face

    def _update3(self, edge1, edge2, edge3):
        """Update structures at a node with the degree greater than 1.
        edge2 is a new edge inserted between edge1 and edge3
        (counterclockwise direction).
        """
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

# EOF
