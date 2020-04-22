#!/usr/bin/python

from planegeometry.algorithms.geomtools import oriented_area

class QuickHull:
    """Quickhull algorithm for finding the convex hull of points.
    
    https://en.wikipedia.org/wiki/Quickhull
    
    Starting point are top and bottom 
    """

    def __init__(self, point_list):
        """The algorithm initialization."""
        if len(point_list) < 3:
            raise ValueError("small number of points")
        self.point_list = point_list
        self.convex_hull = None

    def run(self):
        """Executable pseudocode."""
        pt1 = min(self.point_list, key=lambda p: (p.y, p.x))
        pt2 = max(self.point_list, key=lambda p: (p.y, p.x))
        list1 = self._points_on_the_right(pt1, pt2, self.point_list)
        list2 = self._points_on_the_right(pt2, pt1, self.point_list)
        self.convex_hull = ([pt1] + self._quickhull(pt1, pt2, list1)
                          + [pt2] + self._quickhull(pt2, pt1, list2))

    def _points_on_the_right(self, pt1, pt2, point_list):
        """Return the list of points on the right side of the oriented
        line from pt1 to pt2 (the list may be empty!)."""
        new_list = []
        for pt3 in point_list:
            if oriented_area(pt1, pt2, pt3) < 0:
                new_list.append(pt3)
        return new_list

    def _quickhull(self, pt1, pt2, point_list):
        """Find points on convex hull from the list that are 
        on the right side of the oriented line from pt1 to pt2."""
        if not point_list:
            return []
        pt3 = max(point_list, key=lambda p: oriented_area(pt1, p, pt2))
        # Nie trzeba dzielic przez abs(pt2-pt1).
        list1 = self._points_on_the_right(pt1, pt3, point_list)
        list2 = self._points_on_the_right(pt3, pt2, point_list)
        return (self._quickhull(pt1, pt3, list1) + [pt3]
              + self._quickhull(pt3, pt2, list2))

# EOF
