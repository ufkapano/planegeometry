#!/usr/bin/python

from planegeometry.structures.points import Point
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.edges import Edge
from planegeometry.structures.graphs import Graph


class TriangleCollection:
    """The class defining a triangle collection."""

    def __init__(self):
        """Make a collection of triangles."""
        self.items = []

    def __len__(self):
        """Return the number of triangles in the collection."""
        return len(self.items)

    def itertriangles(self):
        """Generate triangles on demand."""
        for triangle in self.items:
            yield triangle

    def insert(self, triangle):
        """Insert a triangle to the collection."""
        if not isinstance(triangle, Triangle):
            raise ValueError("not a triangle")
        self.items.append(triangle)
        #print ( "tc.insert {}".format(triangle) )

    def remove(self, triangle):
        """Remove a triangle from the collection."""
        self.items.remove(triangle)
        #print ( "tc.remove {}".format(triangle) )

    def search(self, point):
        """Finding triangles containing a point."""
        result = []
        for triangle in self.items:
            if point in triangle:
                result.append(triangle)
        return result

    def to_graph(self):
        """Return the triangulation as a graph."""
        graph = Graph()
        for triangle in self.items:
            edge1 = Edge(triangle.pt1, triangle.pt2)
            edge2 = Edge(triangle.pt1, triangle.pt3)
            edge3 = Edge(triangle.pt2, triangle.pt3)
            for edge in (edge1, edge2, edge3):
                if not graph.has_edge(edge):
                    graph.add_edge(edge)
        return graph

# EOF
