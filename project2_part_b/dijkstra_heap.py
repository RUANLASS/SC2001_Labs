
class MinHeap:
    """Binary min-heap of vertices keyed by tentative distance.

    pos[v] stores the index of vertex v in the heap array (or -1 if v is not
    in the heap), so that decrease_key can locate v in O(1) time.
    """

    def __init__(self, n):
        self.heap = []          # list of (key, vertex)
        self.pos = [-1] * n

    def is_empty(self):
        return len(self.heap) == 0

    def contains(self, v):
        return self.pos[v] != -1

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        size = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest

    def insert(self, v, key):
        self.heap.append((key, v))
        self.pos[v] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        key, v = self.heap[0]
        last = self.heap.pop()
        self.pos[v] = -1

        if self.heap:
            self.heap[0] = last
            self.pos[last[1]] = 0
            self._sift_down(0)

        return v, key

    def decrease_key(self, v, key):
        i = self.pos[v]
        self.heap[i] = (key, v)
        self._sift_up(i)


def dijkstra_heap(graph, source):
    """graph is an array of adjacency lists: graph[u] = [(v, weight), ...]"""
    n = len(graph)

    INF = float('inf')

    # Store the best-known distances
    dist = [INF] * n

    # Track which vertices have been processed
    visited = [False] * n

    # Distance from the source to itself is zero
    dist[source] = 0

    pq = MinHeap(n)
    pq.insert(source, 0)

    while not pq.is_empty():
        u, d = pq.extract_min()
        visited[u] = True
        #print("Selected vertex:", u)

        # Only the actual neighbours of u are examined
        for v, weight in graph[u]:
            if not visited[v]:
                new_dist = d + weight

                if new_dist < dist[v]:
                    dist[v] = new_dist

                    if pq.contains(v):
                        pq.decrease_key(v, new_dist)
                    else:
                        pq.insert(v, new_dist)

    return dist


def main():
    # Array of adjacency lists (same graph as in part a)
    graph = [
        [(1, 4), (3, 10)],
        [(0, 4), (2, 2)],
        [(1, 2), (3, 3)],
        [(0, 10), (2, 3)]
    ]

    # Start at vertex A (index 0)
    source = 0

    dist = dijkstra_heap(graph, source)

    print("Distances from vertex A:", dist)


if __name__ == "__main__":
    main()
