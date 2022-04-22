#!/usr/bin/env python3

class QuadTree:
    """The class defining a quadtree.
    
    https://en.wikipedia.org/wiki/Quadtree
    """

    def __init__(self, rect, capacity=4):
        """Make a quadtree."""
        self.rect = rect   # area for points
        self.capacity = capacity
        self.point_list = []
        # If len(point_list) <= capacity, then there are no children.
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None

    def __str__(self):
        """String representation of a quadtree."""
        return "QuadTree({}, {})".format(self.rect, self.capacity)

    def _is_divided(self):
        """Test if the quadtree is divided."""
        return self.top_left is not None

    def height(self):
        """Return the height of the quadtree."""
        if self._is_divided():
            tl = self.top_left.height()
            tr = self.top_right.height()
            bl = self.bottom_left.height()
            br = self.bottom_right.height()
            return 1 + max(tl, tr, bl, br)
        else:
            return 1

    def insert(self, point):
        """Insert a point into the quadtree."""
        # Ignore points that do not belong in this quadtree.
        if point not in self.rect:
            return False
        # If there is space in this quadtree and if doesn't have subdivisions,
        # add the point here.
        if len(self.point_list) < self.capacity and not self._is_divided():
            self.point_list.append(point)
            return True
        # Otherwise, subdivide and then add the point to whichever node
        # will accept it.
        if not self._is_divided():
            self._subdivide()
        # We have to add the points contained into this quad array
        # to the new quads if we want that only the last node holds the point.
        # Czyli tu mozna przerzucic punkty z point_list do poddrzew.
        # Wtedy tylko liscie beda zawieraly punkty.
        #    while self.point_list:   # option: moving points to leafs
        #        self.insert(self.point_list.pop())
        if self.top_left.insert(point):
            return True
        if self.top_right.insert(point):
            return True
        if self.bottom_left.insert(point):
            return True
        if self.bottom_right.insert(point):
            return True

    def _subdivide(self):
        """Subdividing the currect rect."""
        # Divide rect on 4 equal parts.
        tl, tr, bl, br = self.rect.make4()
        self.top_left = QuadTree(tl, self.capacity)
        self.top_right = QuadTree(tr, self.capacity)
        self.bottom_left = QuadTree(bl, self.capacity)
        self.bottom_right = QuadTree(br, self.capacity)

    def query(self, query_rect):
        """Find all points that appear within a range."""
        points_in_rect = []
        try:
            self.rect.intersection(query_rect)
        except ValueError:
            return []
        # Check points at this quadtree level.
        for pt in self.point_list:
            if pt in query_rect:
                points_in_rect.append(pt)
        # Terminate here, if there are no children.
        if not self._is_divided():
            return points_in_rect
        # Otherwise, add the points from the children.
        children = (self.top_left, self.top_right,
                    self.bottom_left, self.bottom_right)
        for child in children:
            points_in_rect.extend(child.query(query_rect))
        return points_in_rect

    def nearest(self, point, best=None):
        """Find a nearest point."""
        # best to kandydat najlepszy do tej pory znaleziony.
        # Szukanie punktu najblizszego do podanego.
        # http://bl.ocks.org/patricksurry/6478178
        # Jezeli best nie zostal podany, to jestesmy na najwyzszym
        # poziomie i musza byc jakies punkty w obszarze.
        # Czyli tu przyjmuje, ze punkty sa nie tylko w lisciach, ale tez wyzej.
        if best is None:
            best = self.point_list[0]
        distance = (point-best).length()
        # Nie sprawdzamy obszaru, jezeli point jest za daleko.
        if (point.x < self.rect.pt1.x - distance or
            point.x > self.rect.pt2.x + distance or
            point.y < self.rect.pt1.y - distance or
            point.y > self.rect.pt2.y + distance):
                return best
        # Sprawdzenie punktow w wezle.
        for pt in self.point_list:
            new_distance = (point-pt).length()
            if new_distance < distance:
                best = pt
                distance = new_distance
        # Terminate here, if there are no children.
        if not self._is_divided():
            return best
        # Otherwise, check the children.
        # Finding the best children ordering for searching.
        c = self.rect.center()
        if point.x > c.x:   # right, left
            if point.y > c.y:   # top, bottom
                children = (self.top_right, self.top_left,
                            self.bottom_right, self.bottom_left)
            else:   # bottom, top
                children = (self.bottom_right, self.bottom_left,
                            self.top_right, self.top_left)
        else:   # left, right
            if point.y > c.y:   # top, bottom
                children = (self.top_left, self.top_right,
                            self.bottom_left, self.bottom_right)
            else:   # bottom, top
                children = (self.bottom_left, self.bottom_right,
                            self.top_left, self.top_right)
        for child in children:
            best = child.nearest(point, best)
        return best

# EOF
