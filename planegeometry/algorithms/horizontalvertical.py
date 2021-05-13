#!/usr/bin/python
#
# Wygodnie jest events sortowac po y, bo potem miotla automatycznie
# sortuje po x. Miotla przesuwa sie z dolu do gory.
# Poczatkowe sortowanie events po y to czas O(n log n).
# Znajdowanie odcinkow pionowych przecinanych przez poziomy robie
# przez successor() w czasie O(log n).
# Wszystkie k przeciec znajde w czasie O(k log n).
# Sumaryczna zlozonosc algorytmu to O((n+k)log n).

from planegeometry.structures.events import Event
from planegeometry.structures.avltree1 import AVLTree


class HorizontalVertical:
    """Intersections of horizontal and vertical line segments."""

    def __init__(self, segment_list):
        """Initialize structures."""
        self.event_queue = []  # sorted along y
        self.sweep_line = AVLTree()  # sorted along x

        for segment in segment_list:   # O(n) time
            if segment.pt1 > segment.pt2:
                # (x1 > x2 and y1 = y2) or (x1 = x2 and y1 > y2)
                segment = ~segment
            if segment.pt1.x == segment.pt2.x:   # vertical segment
                self.event_queue.append(Event(segment.pt1, Event.BOTTOM, segment))
                self.event_queue.append(Event(segment.pt2, Event.TOP, segment))
            elif segment.pt1.y == segment.pt2.y:   # horizontal segment
                self.event_queue.append(Event(segment.pt1, Event.HORIZONTAL, segment))
            else:
                raise ValueError("horizontal or vertical segments are allowed")

        self.event_queue.sort(key=lambda event: event.point.y)   # O(n log n) time
        self.il = []   # intersection list

    def run(self):
        """Processing events."""
        for event in self.event_queue:
            if event.type == Event.BOTTOM:
                self._handle_bottom_endpoint(event)
            elif event.type == Event.TOP:
                self._handle_top_endpoint(event)
            elif event.type == Event.HORIZONTAL:
                self._handle_crossing(event)
            else:
                raise ValueError("unknown event")
        del self.event_queue
        del self.sweep_line
        return self.il

    def _handle_bottom_endpoint(self, event):
        self.sweep_line.insert(event.segment)   # O(log n) time

    def _handle_top_endpoint(self, event):
        self.sweep_line.remove(event.segment)   # O(log n) time

    def _handle_crossing(self, event):
        # Trzeba sprawdzic jakie pionowe odcinki przecina ten poziomy.
        # Musze zaznaczyc poczatkowy x.
        segment_e = event.segment
        x_min = segment_e.pt1.x
        x_max = segment_e.pt2.x
        self.sweep_line.insert(segment_e)   # O(log n) time

        node = self.sweep_line.successor(segment_e)   # O(log n) time
        # Dopoki sa odcinki pionowe w zakresie ...
        while node and node.value.pt1.x < x_max:
            # Znajdz punkt przeciecia.
            point = segment_e.intersection_point(node.value)
            self.il.append(point)
            # Przesun dalej w prawo.
            node = self.sweep_line.successor(node.value)   # O(log n) time

        # No koncu usuwam poziomy segment.
        self.sweep_line.remove(segment_e)   # O(log n) time
