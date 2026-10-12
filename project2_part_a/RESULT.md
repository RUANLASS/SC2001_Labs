# Project 2 Part (a): Array-based Dijkstra — averaged results

Averaged over **5 seeds (1–5)**; the original scripts use a fixed seed of 42, which the driver replaced per run. Each per-seed time is itself a mean of 5 repetitions. Values are mean ± sample std. dev. across seeds. Raw per-seed data: [results_seeds.csv](results_seeds.csv).

Adjacency matrix + array priority queue, O(V²).

## Varying |V| (edge probability 0.3)

| Vertices | Avg edges | Avg time (s) |
|---|---|---|
| 100 | 1485 | 0.000843 ± 0.000010 |
| 200 | 5958 | 0.003224 ± 0.000020 |
| 400 | 23928 | 0.013496 ± 0.000142 |
| 800 | 95814 | 0.055831 ± 0.000622 |
