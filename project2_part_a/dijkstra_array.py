
def dijkstra_array(graph, source):
    n = len(graph)

    INF = float('inf')

    # Store the best-known distances
    dist = [INF] * n

    # Track which vertices have been processed
    visited = [False] * n

    # Distance from the source to itself is zero
    dist[source] = 0

    for count in range(n):
        u = -1
        min_dist = INF

        for v in range(n):
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u == -1:
            break

        visited[u] = True
        #print("Selected vertex:", u)

        for v in range(n):
            if not visited[v] and graph[u][v] != 0:
                new_dist = dist[u] + graph[u][v]

                if new_dist < dist[v]:
                    dist[v] = new_dist


    return dist 


def main():
    # Adjacency matrix
    graph = [
        [0,  4,  0,  10],
        [4,  0,  2,   0],
        [0,  2,  0,   3],
        [10, 0,  3,   0]
    ]

    # Start at vertex A (index 0)
    source = 0

    dist = dijkstra_array(graph, source)

    print("Distances from vertex A:", dist)


if __name__ == "__main__":
    main()
