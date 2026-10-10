
import csv
import os
import random
import sys
import time

# Import the part (a) and part (b) implementations directly
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "project2_part_a"))
sys.path.append(os.path.join(HERE, "..", "project2_part_b"))

import dijkstra_heap as heap_module
from dijkstra_array import dijkstra_array
from dijkstra_heap import MinHeap, dijkstra_heap

REPETITIONS = 5
RESULTS_CSV = os.path.join(HERE, "results.csv")


def generate_graph(n, probability=0.3):
    """Generate a random undirected graph stored as an adjacency matrix.

    Same procedure as parts (a) and (b), so the same seed gives the same graphs.
    """
    graph = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < probability:
                weight = random.randint(1, 20)
                graph[i][j] = weight
                graph[j][i] = weight

    return graph


def generate_worst_case_graph(n):
    """Generate a complete graph where every edge examination improves a distance.

    Edge (i, i+1) has weight 1, so dist[v] = v and vertices are extracted in
    the order 0, 1, ..., n-1. Every other edge (i, j) with j > i + 1 has weight
    n*(n-i) - j - i, so dist[i] + w(i, j) = n*(n-i) - j, which is smaller than
    the tentative distance set by any earlier vertex. Each time vertex i is
    extracted, every unvisited vertex therefore gets an insert or decrease_key,
    giving |V|(|V|-1)/2 heap updates: the worst case for part (b).
    """
    graph = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            weight = 1 if j == i + 1 else n * (n - i) - j - i
            graph[i][j] = weight
            graph[j][i] = weight

    return graph


def matrix_to_adj_list(matrix):
    """Convert an adjacency matrix to an array of adjacency lists (as in part b)."""
    n = len(matrix)
    adj = [[] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                adj[i].append((j, matrix[i][j]))

    return adj


def count_edges(adj):
    """Count each undirected edge once."""
    return sum(len(neighbours) for neighbours in adj) // 2


class CountingMinHeap(MinHeap):
    """MinHeap that counts heap updates. Used only in an untimed run."""

    def __init__(self, n):
        super().__init__(n)
        self.inserts = 0
        self.decrease_keys = 0

    def insert(self, v, key):
        self.inserts += 1
        super().insert(v, key)

    def decrease_key(self, v, key):
        self.decrease_keys += 1
        super().decrease_key(v, key)


def count_heap_operations(adj):
    """Run part (b) once with a counting heap and return (inserts, decrease_keys)."""
    heaps = []

    def make_heap(n):
        heaps.append(CountingMinHeap(n))
        return heaps[-1]

    heap_module.MinHeap = make_heap
    try:
        dijkstra_heap(adj, 0)
    finally:
        heap_module.MinHeap = MinHeap

    return heaps[0].inserts, heaps[0].decrease_keys


def measure_both(matrix, adj):
    """Average execution time of both implementations on the same graph.

    The two implementations alternate on every repetition, so both see the
    same machine conditions within a single run of this script.
    """
    array_times = []
    heap_times = []

    for _ in range(REPETITIONS):
        start = time.perf_counter()
        dist_array = dijkstra_array(matrix, 0)
        array_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        dist_heap = dijkstra_heap(adj, 0)
        heap_times.append(time.perf_counter() - start)

    assert dist_array == dist_heap, "part (a) and part (b) disagree"

    return sum(array_times) / REPETITIONS, sum(heap_times) / REPETITIONS


def run_case(experiment, n, probability, matrix, rows):
    adj = matrix_to_adj_list(matrix)
    edges = count_edges(adj)
    array_time, heap_time = measure_both(matrix, adj)
    inserts, decrease_keys = count_heap_operations(adj)
    ratio = array_time / heap_time
    faster = "heap (b)" if heap_time < array_time else "array (a)"

    rows.append({
        "experiment": experiment,
        "vertices": n,
        "edge_probability": probability,
        "edges": edges,
        "array_time_s": f"{array_time:.6f}",
        "heap_time_s": f"{heap_time:.6f}",
        "array_over_heap": f"{ratio:.2f}",
        "heap_inserts": inserts,
        "heap_decrease_keys": decrease_keys,
        "faster": faster,
    })

    label = f"{probability:>5}" if experiment != "worst_case" else "worst"
    print(f"{n:5} | {label} | {edges:7} | {array_time:10.6f} | {heap_time:10.6f} | "
          f"{ratio:6.2f} | {decrease_keys:7} | {faster}")


def print_header(title):
    print(title)
    print("  |V| |     p |     |E| |  array (s) |   heap (s) | a / b  | dec-key | faster")
    print("-------------------------------------------------------------------------------")


def experiment_vary_vertices(rows):
    """Experiment 1: vary |V| at edge probability 0.3.

    With seed 42, the first four graphs are exactly those used in parts (a) and (b).
    """
    random.seed(42)
    print_header("Experiment 1: varying |V| (edge probability = 0.3)")

    for n in [100, 200, 400, 800, 1600]:
        run_case("vary_vertices", n, 0.3, generate_graph(n, probability=0.3), rows)

    print()


def experiment_vary_density(rows):
    """Experiment 2: fix |V| = 1000 and vary the edge probability from sparse to complete."""
    random.seed(42)
    n = 1000
    print_header(f"Experiment 2: varying edge probability (|V| = {n})")

    for p in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        run_case("vary_density", n, p, generate_graph(n, probability=p), rows)

    print()


def experiment_worst_case(rows):
    """Experiment 3: complete graphs whose weights force a heap update on every edge."""
    print_header("Experiment 3: worst-case complete graphs (every edge triggers a heap update)")

    for n in [100, 200, 400, 800, 1000]:
        run_case("worst_case", n, 1.0, generate_worst_case_graph(n), rows)

    print()


def main():
    rows = []
    experiment_vary_vertices(rows)
    experiment_vary_density(rows)
    experiment_worst_case(rows)

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results written to {RESULTS_CSV}")


if __name__ == "__main__":
    main()
