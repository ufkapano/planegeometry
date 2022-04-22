#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

from planegeometry.algorithms.geomtools import find_two_closest_points


class ClosestPairDivideConquer:
    """Solving the closest pair problem using divide and conquer.
    
    https://www.geeksforgeeks.org/closest-pair-of-points-using-divide-and-conquer-algorithm/
    Complexity O(n (log n)^2).
    """

    def __init__(self, point_list):
        if len(point_list) < 2:
            raise ValueError("minimum 2 points")
        self.point_list = point_list
        self.point_list.sort()
        self.closest_pair = None
        self.min_distance = None

    def run(self):
        self.closest_pair = self._closest(0, len(self.point_list)-1)
        self.min_distance = self.pair_length(self.closest_pair)
        return self.closest_pair

    def _closest(self, left, right):
        # Wywolania rekurencyjne beda pracowac na roznych zakresach
        # tej samej listy, aby niepotrzebnie nie kopiowac punktow.
        if (right - left) <= 2:
            return find_two_closest_points(self.point_list[left:right+1])

        middle = (left + right) // 2
        closest_left = self._closest(left, middle)
        closest_right = self._closest(middle + 1, right)
        left_d = self.pair_length(closest_left)
        right_d = self.pair_length(closest_right)

        if left_d < right_d:
            closest_pair = closest_left
            current_d = left_d
        else:
            closest_pair = closest_right
            current_d = right_d
        # Build a strip (the width is 2*d).
        strip = []
        for i in range(left, right+1):   # O(n) time
            if abs(self.point_list[middle].x - self.point_list[i].x) < current_d:
                strip.append(self.point_list[i])

        if len(strip) < 2:   # moze byc malo punktow w pasie
            closest_strip = closest_pair
        else:
            closest_strip = self._closest_on_strip(strip, current_d)

        if current_d < self.pair_length(closest_strip):
            return closest_pair
        else:
            return closest_strip

    def _closest_on_strip(self, strip, distance):
        min_distance = distance
        strip.sort(key=lambda point: point.y)
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
