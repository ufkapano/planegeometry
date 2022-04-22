#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

from planegeometry.algorithms.geomtools import find_two_closest_points


class ClosestPairSortXY:
    """Solving the closest pair problem using divide and conquer.
    
    Complexity O(n log n). The idea is from 
    Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C., 2009, 
        Introduction to Algorithms, third edition, The MIT Press, 
        Cambridge, London.
    """

    def __init__(self, point_list):
        if len(point_list) < 2:
            raise ValueError("minimum 2 points")
        self.P = set(point_list)
        self.closest_pair = None
        self.min_distance = None

    def run(self):
        # Obok zbioru punktow P potrzebujemy dwie listy tych punktow,
        # posortowane po x i posortowane po y.
        X = list(self.P)
        X.sort(key=lambda point: point.x)   # O(n log n) time
        Y = list(self.P)
        Y.sort(key=lambda point: point.y)   # O(n log n) time
        self.closest_pair = self._closest(self.P, X, Y)
        self.min_distance = self.pair_length(self.closest_pair)
        return self.closest_pair

    def _closest(self, P, X, Y):
        if len(P) <= 3:
            return find_two_closest_points(X)

        middle = len(P) // 2
        middle_point = X[middle]
        X_left = X[:middle]
        X_right = X[middle:]
        P_left = set(X_left)
        P_right = set(X_right)
        # Dziele punkty zachowujac posortowanie wzgledem y.
        Y_left = []
        Y_right = []
        for point in Y:   # O(n) time
            if point in P_left:   # szybkie dzieki zbiorom
                Y_left.append(point)
            else:
                Y_right.append(point)
        closest_left = self._closest(P_left, X_left, Y_left)
        closest_right = self._closest(P_right, X_right, Y_right)
        left_d = self.pair_length(closest_left)
        right_d = self.pair_length(closest_right)

        if left_d < right_d:
            closest_pair = closest_left
            current_d = left_d
        else:
            closest_pair = closest_right
            current_d = right_d
        # Build a strip (the width is 2*d).
        # strip ma byc juz posortowany wzgledem y!
        strip = []
        for point in Y:   # O(n) time
            if abs(middle_point.x - point.x) < current_d:
                strip.append(point)

        if len(strip) < 2:   # moze byc malo punktow w pasie
            closest_strip = closest_pair
        else:
            closest_strip = self._closest_on_strip(strip, current_d)

        if current_d < self.pair_length(closest_strip):
            return closest_pair
        else:
            return closest_strip

    def _closest_on_strip(self, strip, distance):   # O(n) time
        min_distance = distance
        closest_pair = strip[0], strip[1]
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                # Roznica wspolrzednych y ma byc nie wieksza od d.
                # Druga petla przebiegnie najwyzej 7(?) razy.
                if strip[j].y - strip[i].y > min_distance:
                    break
                new_distance = (strip[i] - strip[j]).length()
                if new_distance < min_distance:
                    min_distance = new_distance
                    closest_pair = strip[i], strip[j]
        return closest_pair

    def pair_length(self, pair):
        return (pair[0] - pair[1]).length()
