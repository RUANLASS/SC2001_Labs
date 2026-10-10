
# SC2001 Project 2: Dijkstra's Algorithm

## Part (b): Array of Adjacency Lists and Minimizing Heap Priority Queue

### 1. Implementation

The graph is represented as an array of adjacency lists, where `graph[u]` stores a list of `(v, weight)` pairs for every edge leaving vertex `u`. The priority queue is a binary min-heap keyed by tentative distance, implemented in the `MinHeap` class in `dijkstra_heap.py`.

The heap supports three operations:

- `insert(v, key)`: append the vertex at the end of the heap and sift it up.
- `extract_min()`: remove the root, move the last element to the root and sift it down.
- `decrease_key(v, key)`: update the key of `v` and sift it up.

To support `decrease_key`, the heap keeps a position array `pos`, where `pos[v]` is the index of vertex `v` in the heap (or -1 if `v` is not in the heap). This lets the algorithm find a vertex in the heap in O(1) time instead of searching for it.

The algorithm starts with only the source in the heap. It repeatedly extracts the vertex `u` with the smallest tentative distance, marks it as visited and relaxes each edge `(u, v)` in `u`'s adjacency list. When a shorter path to `v` is found, `v` is inserted into the heap if it is not already there, or its key is decreased if it is. Since each vertex enters the heap at most once, the heap never holds more than |V| elements.

### 2. Theoretical Time Complexity

Initialising the distance and visited arrays takes O(|V|) time.

**Extracting the minimum.** Each vertex is inserted into and extracted from the heap at most once. A heap with at most |V| elements has height O(log |V|), so each `insert` and `extract_min` takes O(log |V|) time. Over all vertices this costs O(|V| log |V|).

**Relaxing edges.** Each vertex is extracted once, and its adjacency list is scanned once at that point. Over the whole run, every adjacency list is scanned exactly once, so the total number of edge examinations is the sum of all vertex degrees: |E| for a directed graph, or 2|E| for an undirected graph. Each examination takes O(1) time, plus one `decrease_key` costing O(log |V|) when the distance improves. In the worst case every edge examination causes a `decrease_key`, which costs O(|E| log |V|).

Therefore, the overall worst-case time complexity is

**O((|V| + |E|) log |V|)**, which is O(|E| log |V|) when the graph is connected (|E| ≥ |V| − 1).

Unlike part (a), this complexity depends on the number of edges: the adjacency list stores only the edges that exist, so the algorithm never examines absent edges. For a sparse graph with |E| = O(|V|), the cost is O(|V| log |V|). For a dense graph with |E| = Θ(|V|²), the cost becomes O(|V|² log |V|), which is asymptotically worse than the O(|V|²) of part (a).

The adjacency lists use O(|V| + |E|) space, compared with O(|V|²) for the adjacency matrix.

### 3. Empirical Time Complexity

The experiments use the same random graph generator as part (a): each pair of vertices is connected with a fixed probability, and edge weights are random integers between 1 and 20. Each graph is generated as a matrix and then converted to adjacency lists; the conversion time is not measured. With the same random seed (42), experiment 1 produces exactly the same graphs as part (a), so the two sets of results can be compared directly. Each measurement is the average of five runs timed with `time.perf_counter()`.

Before timing, `experiment.py` checks correctness by running both the part (a) and part (b) implementations on 12 random graphs (|V| from 5 to 100, edge probability from 0.05 to 0.8) and confirming that they return identical distances.

The last column of each table divides the measured time by (|V| + |E|) log₂|V|. If the running time grew exactly in proportion to the theoretical bound, this value would stay roughly constant.

**Experiment 1: varying |V| (edge probability = 0.3)**

| Number of vertices (\|V\|) | Number of edges (\|E\|) | Average execution time (seconds) | time / ((V+E) log V) (ns) |
|---:|---:|---:|---:|
| 100 | 1,462 | 0.000492 | 47.36 |
| 200 | 5,966 | 0.001293 | 27.44 |
| 400 | 23,909 | 0.003635 | 17.30 |
| 800 | 95,824 | 0.012092 | 12.98 |

**Experiment 2: varying |E| (|V| = 1000)**

| Edge probability | Number of edges (\|E\|) | Average execution time (seconds) | time / ((V+E) log V) (ns) |
|---:|---:|---:|---:|
| 0.005 | 2,532 | 0.004762 | 135.28 |
| 0.01 | 5,018 | 0.005386 | 89.80 |
| 0.05 | 24,993 | 0.007291 | 28.15 |
| 0.1 | 50,042 | 0.009268 | 18.22 |
| 0.2 | 100,285 | 0.013681 | 13.55 |
| 0.4 | 199,935 | 0.022104 | 11.04 |
| 0.8 | 399,501 | 0.040300 | 10.10 |

In experiment 2, the number of vertices is fixed and the execution time increases steadily with the number of edges, from 0.0048 seconds at about 2,500 edges to 0.0403 seconds at about 400,000 edges. This confirms that the running time of this implementation depends on |E|, unlike part (a). Between p = 0.2 and p = 0.8, |E| increases about 4 times and the time increases about 2.9 times, so for dense graphs the growth is close to linear in |E|.

In both experiments, the normalised ratio decreases as the graph grows. This means the measured time grows more slowly than (|V| + |E|) log |V|, so the bound holds but is not tight for these inputs. There are two reasons:

1. **Few edges trigger `decrease_key`.** The O(|E| log |V|) term assumes every edge examination causes a heap update. To check this, the heap operations were counted for the graphs in experiment 2:

   | Edge probability | \|E\| | Inserts | Decrease-keys |
   |---:|---:|---:|---:|
   | 0.005 | 2,532 | 994 | 404 |
   | 0.05 | 24,993 | 1,000 | 1,777 |
   | 0.2 | 100,285 | 1,000 | 2,102 |
   | 0.8 | 399,501 | 1,000 | 2,263 |

   Even with about 400,000 edges, only about 2,300 relaxations improved a distance. In a dense graph with random weights, most vertices get a short tentative distance early on, so later edges rarely improve it. As a result, the log |V| cost is paid for only a few thousand heap operations, and the main cost is the O(1) check on each edge. For these graphs the running time behaves more like O(|E| + |V| log |V|).

2. **Fixed overheads matter more for small graphs.** For small or sparse graphs, Python's per-call costs, such as function calls and loop setup, take up a larger share of the total time, which raises the ratio for the smallest inputs.

The worst case, where almost every edge triggers a `decrease_key`, requires carefully constructed edge weights and does not appear in random graphs.

As in part (a), the graph generator does not guarantee connectivity, and the timings depend on the hardware used. For the sparsest graph (p = 0.005), only 994 of the 1,000 vertices were reachable from the source.

### 4. Discussion

The adjacency-list representation lets the algorithm examine only the edges that exist, and the min-heap reduces the cost of selecting the next vertex from O(|V|) to O(log |V|). Together, these give a worst-case time complexity of O((|V| + |E|) log |V|), which depends on both the number of vertices and the number of edges.

The experiments confirm that the running time grows with |E| when |V| is fixed. They also show that, for random graphs, the measured growth stays below the theoretical bound, because only a small fraction of edges lead to a `decrease_key`.

On the same graphs used in part (a) (experiment 1), the heap-based implementation was faster at every size tested. When both were run on the same machine, the heap version took 0.012 seconds for |V| = 800 at edge probability 0.3, a fairly dense graph, compared with 0.055 seconds for the array version. (The part (a) report lists 0.074 seconds, measured on a different machine.) The comparison between the two implementations, and when each one is preferable, is discussed in part (c).
