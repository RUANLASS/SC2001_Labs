
import math
import os
import random
import sys
import time
from dijkstra_heap import dijkstra_heap

# Allow importing the part (a) implementation for a correctness check
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "project2_part_a"))
from dijkstra_array import dijkstra_array


def generate_graph(n, probability=0.3):
    """Generate a random undirected graph stored as an adjacency matrix.

    Uses the same procedure as part (a), so the same seed gives the same graphs.
    """
    graph = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < probability:
                weight = random.randint(1, 20)
                graph[i][j] = weight
                graph[j][i] = weight

    return graph


def matrix_to_adj_list(matrix):
    """Convert an adjacency matrix to an array of adjacency lists."""
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


def measure_time(adj, repetitions=5):
    """Measure the average execution time of Dijkstra's algorithm."""
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()
        dijkstra_heap(adj, 0)
        end = time.perf_counter()
        times.append(end - start)

    return sum(times) / len(times)


def check_correctness():
    """Check that part (a) and part (b) produce identical distances."""
    random.seed(0)

    for n in [5, 20, 50, 100]:
        for p in [0.05, 0.3, 0.8]:
            matrix = generate_graph(n, probability=p)
            adj = matrix_to_adj_list(matrix)
            assert dijkstra_array(matrix, 0) == dijkstra_heap(adj, 0)

    print("Correctness check passed: heap results match array results.\n")


def experiment_vary_vertices():
    """Experiment 1: vary |V| with edge probability fixed at 0.3 (as in part a)."""
    random.seed(42)

    sizes = [100, 200, 400, 800]

    print("Experiment 1: varying |V| (edge probability = 0.3)")
    print("Vertices | Edges | Average time (seconds) | time / ((V+E) log V) (ns)")
    print("---------------------------------------------------------------------")

    for n in sizes:
        adj = matrix_to_adj_list(generate_graph(n, probability=0.3))
        edges = count_edges(adj)
        avg_time = measure_time(adj)
        ratio = avg_time / ((n + edges) * math.log2(n)) * 1e9

        print(f"{n:8} | {edges:5} | {avg_time:22.6f} | {ratio:.2f}")

    print()


def experiment_vary_edges():
    """Experiment 2: fix |V| = 1000 and vary |E| through the edge probability."""
    random.seed(42)

    n = 1000
    probabilities = [0.005, 0.01, 0.05, 0.1, 0.2, 0.4, 0.8]

    print(f"Experiment 2: varying |E| (|V| = {n})")
    print("Probability | Edges | Average time (seconds) | time / ((V+E) log V) (ns)")
    print("------------------------------------------------------------------------")

    for p in probabilities:
        adj = matrix_to_adj_list(generate_graph(n, probability=p))
        edges = count_edges(adj)
        avg_time = measure_time(adj)
        ratio = avg_time / ((n + edges) * math.log2(n)) * 1e9

        print(f"{p:11} | {edges:6} | {avg_time:22.6f} | {ratio:.2f}")

    print()


def main():
    check_correctness()
    experiment_vary_vertices()
    experiment_vary_edges()


if __name__ == "__main__":
    main()
