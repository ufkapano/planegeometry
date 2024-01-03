#!/usr/bin/env python3
#
# Symulacja drzewa AVL w celu sprawdzenia dzialania kodu.
# Nie pozwala na wstawienie powtarzajacego sie elementu.
# Ale Y-struktura nie zajmuje sie powtarzajacymi sie elementami!
# Klasa Node symuluje wezel drzewa AVL.
# Zachodzi segment.pt1 < segment.pt2 (porownywanie X, potem Y).

class Node:
    """The class defining a node with a segment."""

    def __init__(self, segment):
        self.value = segment

    def __repr__(self):
        return "Node({})".format(self.value)


class SlowTreeY:
    """AVL tree simulation for segment intersection problem.
    Segments are sorted according to Y.
    """

    def __init__(self):
        self.items = []
        self.D = dict()   # fast finding nodes

    def __str__(self):
        return str(self.items)

    def insert(self, segment):
        # Kiedy wstawiamy odcinek, to zdarzeniem jest poczatek odcinka.
        # Miotla idzie z lewej na prawo.
        current_x = min(segment.pt1.x, segment.pt2.x)
        new_node = Node(segment)
        self.items.append(new_node)
        self.D[segment] = new_node
        # Sortowanie wezlow po wartosciach Y (przeciecie odcinka z miotla).
        # W drzewie AVL bedzie zejsie od korzenia w dol.
        self.items.sort(key=lambda node: node.value.calculate_y(current_x))

    def remove(self, segment):
        # Jezeli nie ma na liscie to ValueError.
        # Zdarzenie to koniec odcinka (pt = segment.pt2).
        # Tu nie potrzebuje pt, ale w drzewie chyba bedzie potrzebne.
        node = self.D[segment]
        del self.D[segment]
        self.items.remove(node)

    def find(self, segment):
        # Dla segmentu szukamy jego node.
        # W drzewie to moze zalezec od punktu zdarzenia, bo musimy
        # isc od korzenia w dol.
        return self.D[segment]

    def swap(self, segment1, segment2):
        # Tu jest dobrze, bo czas O(1).
        node1 = self.D[segment1]
        node2 = self.D[segment2]
        # Zamiana value (odcinkow).
        node1.value, node2.value = node2.value, node1.value
        # Zamiana w slowniku.
        self.D[segment1], self.D[segment2] = self.D[segment2], self.D[segment1]

    def find_min(self):   # zwraca caly wezel
        # W drzewie AVL czas O(log n), tutaj O(1).
        if self.items:
            return self.items[0]
        else:
            raise ValueError("slow tree is empty")

    def find_max(self):   # zwraca wezel
        # W drzewie AVL czas O(log n), tutaj O(1).
        if self.items:
            return self.items[-1]
        else:
            raise ValueError("slow tree is empty")

    def successor(self, segment):   # zwraca wezel lub None
        # Trzeba sie dostac do nastepnika w czasie O(log n).
        # Da sie to zrobic w drzewie AVL, tutaj czas O(n).
        if self.items:
            idx = None
            for i, node in enumerate(self.items):
                if node.value == segment:
                    idx = i
                    break
            return self.items[idx+1] if idx+1 < len(self.items) else None
        else:
            raise ValueError("slowtree is empty")

    def predecessor(self, segment):   # zwraca wezel lub None
        # Trzeba sie dostac do poprzednika w czasie O(log n).
        # Da sie to zrobic w drzewie AVL, tutaj czas O(n).
        if self.items:
            idx = None
            for i, node in enumerate(self.items):
                if node.value == segment:
                    idx = i
                    break
            return self.items[idx-1] if idx > 0 else None
        else:
            raise ValueError("slow tree is empty")

    def empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


class SlowTreeX:
    """AVL tree simulation for segment intersection problem.
    Segments are sorted according to X.
    """

    def __init__(self):
        self.items = []
        self.D = dict()   # fast finding nodes

    def __str__(self):
        return str(self.items)

    def insert(self, segment):
        # Kiedy wstawiamy odcinek, to zdarzeniem jest gorny wierzcholek odcinka.
        # Miotla idzie z gory na dol.
        current_y = max(segment.pt1.y, segment.pt2.y)
        new_node = Node(segment)
        self.items.append(new_node)
        self.D[segment] = new_node
        # Sortowanie wezlow po wartosciach X (przeciecie odcinka z miotla).
        # W drzewie AVL bedzie zejsie od korzenia w dol.
        self.items.sort(key=lambda node: node.value.calculate_x(current_y))

    def remove(self, segment):
        # Jezeli nie ma na liscie to ValueError.
        # Zdarzenie to koniec odcinka (pt = segment.pt2).
        # Tu nie potrzebuje pt, ale w drzewie chyba bedzie potrzebne.
        node = self.D[segment]
        del self.D[segment]
        self.items.remove(node)

    def find(self, segment):
        # Dla segmentu szukamy jego node.
        # W drzewie to moze zalezec od punktu zdarzenia, bo musimy
        # isc od korzenia w dol.
        return self.D[segment]

    def swap(self, segment1, segment2):
        # Tu jest dobrze, bo czas O(1).
        node1 = self.D[segment1]
        node2 = self.D[segment2]
        # Zamiana value (odcinkow).
        node1.value, node2.value = node2.value, node1.value
        # Zamiana w slowniku.
        self.D[segment1], self.D[segment2] = self.D[segment2], self.D[segment1]

    def find_min(self):   # zwraca caly wezel
        # W drzewie AVL czas O(log n), tutaj O(1).
        if self.items:
            return self.items[0]
        else:
            raise ValueError("slow tree is empty")

    def find_max(self):   # zwraca wezel
        # W drzewie AVL czas O(log n), tutaj O(1).
        if self.items:
            return self.items[-1]
        else:
            raise ValueError("slow tree is empty")

    def successor(self, segment):   # zwraca wezel lub None
        # Trzeba sie dostac do nastepnika w czasie O(log n).
        # Da sie to zrobic w drzewie AVL, tutaj czas O(n).
        if self.items:
            idx = None
            for i, node in enumerate(self.items):
                if node.value == segment:
                    idx = i
                    break
            return self.items[idx+1] if idx+1 < len(self.items) else None
        else:
            raise ValueError("slowtree is empty")

    def predecessor(self, segment):   # zwraca wezel lub None
        # Trzeba sie dostac do poprzednika w czasie O(log n).
        # Da sie to zrobic w drzewie AVL, tutaj czas O(n).
        if self.items:
            idx = None
            for i, node in enumerate(self.items):
                if node.value == segment:
                    idx = i
                    break
            return self.items[idx-1] if idx > 0 else None
        else:
            raise ValueError("slow tree is empty")

    def empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

# EOF
