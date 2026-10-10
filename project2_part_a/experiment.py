
import random
import time
from dijkstra_array import dijkstra_array


def generate_graph(n, probability=0.3):
    """Generate a random undirected graph stored as an adjacency matrix."""
    graph = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < probability:
                weight = random.randint(1, 20)
                graph[i][j] = weight
                graph[j][i] = weight

    return graph


def count_edges(graph):
    """Count each undirected edge once."""
    n = len(graph)
    edges = 0

    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] != 0:
                edges += 1

    return edges


def measure_time(graph, repetitions=5):
    """Measure the average execution time of Dijkstra's algorithm."""
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()
        dijkstra_array(graph, 0)
        end = time.perf_counter()
        times.append(end - start)

    return sum(times) / len(times)


def main():
    random.seed(42)

    sizes = [100, 200, 400, 800]

    print("Vertices | Edges | Average time (seconds)")
    print("-----------------------------------------")

    for n in sizes:
        graph = generate_graph(n, probability=0.3)
        edges = count_edges(graph)
        avg_time = measure_time(graph)

        print(f"{n:8} | {edges:5} | {avg_time:.6f}")


if __name__ == "__main__":
    main()
