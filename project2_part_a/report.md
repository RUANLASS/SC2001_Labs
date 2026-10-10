
# SC2001 Project 2: Dijkstra's Algorithm

## Part (a): Adjacency Matrix and Array Priority Queue

### 1. Implementation

The graph is represented using an adjacency matrix. An ordinary array-style scan is used to select the unvisited vertex with the smallest tentative distance.

### 2. Theoretical Time Complexity

The graph is represented using an adjacency matrix, while an ordinary array-based scan is used to select the unvisited vertex with the smallest tentative distance.

Initialising the distance and visited arrays takes (O(|V|)) time. The minimum-distance selection scans all vertices and may be repeated up to (|V|) times, resulting in (O(|V|^2)) time. Similarly, for each selected vertex, the algorithm scans an entire row of the adjacency matrix to examine possible neighbours. Since there are up to (|V|) vertices, this also takes (O(|V|^2)) time.

Therefore, the overall worst-case time complexity is (O(|V|^2)). This complexity is independent of the number of edges because the adjacency matrix requires examining all possible destinations, including those without an edge.

### 3. Empirical Time Complexity

The empirical time complexity was evaluated using randomly generated undirected graphs represented by adjacency matrices. The probability of an edge existing between two vertices was set to 0.3, and edge weights were randomly assigned integers between 1 and 20. Graphs with different numbers of vertices were generated to measure the execution time of the Dijkstra implementation.

Each experiment was repeated five times, and the average execution time was recorded using Python's time.perf_counter() function. A fixed random seed of 42 was used to make the graph generation reproducible.

| Number of vertices (|V|) | Number of edges (|E|) | Average execution time (seconds) |
|---:|---:|---:|
| 100 | 1,462 | 0.002421 |
| 200 | 5,966 | 0.006711 |
| 400 | 23,909 | 0.018556 |
| 800 | 95,824 | 0.073862 |

The results show that execution time increases as the number of vertices increases. When the number of vertices increases from 100 to 800, the average execution time increases from 0.002421 seconds to 0.073862 seconds. This is consistent with the theoretical worst-case time complexity of O(|V|²).

However, execution times may vary depending on the computer's hardware and the structure of the generated graphs. Since the graph generator does not guarantee connectivity, some executions may terminate early when unreachable vertices remain. Therefore, these measurements provide an initial empirical observation rather than a definitive demonstration of worst-case performance.

### 4. Discussion

The experimental results show that the execution time increases as the number of vertices increases. When the number of vertices increases from 100 to 800, the execution time increases from 0.002421 seconds to 0.073862 seconds. This is consistent with the theoretical time complexity of O(|V|²), as the algorithm repeatedly scans the vertices to select the unvisited vertex with the smallest tentative distance and examines each selected vertex's entire row in the adjacency matrix.

Although the number of edges increases as the graph size increases, the algorithm still examines all possible neighbours of each selected vertex, including vertices that are not directly connected to it. Therefore, the time complexity of this implementation is primarily determined by the number of vertices rather than the number of existing edges.

The adjacency matrix and array-based approach is relatively straightforward to implement and is suitable for dense graphs, where many possible edges exist. However, scanning the entire row of the adjacency matrix can be inefficient for sparse graphs, where relatively few edges exist. An adjacency-list representation can avoid examining absent edges, making it potentially more efficient for sparse graphs when combined with an appropriate priority queue.

The measured execution times may vary due to hardware and graph structure. Furthermore, the graph generator does not guarantee connectivity, so the algorithm may terminate early if some vertices are unreachable. Thus, the results provide an initial indication of the algorithm's performance and are broadly consistent with its theoretical complexity.
