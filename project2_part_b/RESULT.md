# Project 2 Part (b): Heap-based Dijkstra — averaged results

Averaged over **5 seeds (1–5)**; the original scripts use a fixed seed of 42, which the driver replaced per run. Each per-seed time is itself a mean of 5 repetitions. Values are mean ± sample std. dev. across seeds. Raw per-seed data: [results_seeds.csv](results_seeds.csv).

Adjacency list + min-heap, O((V+E) log V). Correctness check against part (a) passed in every run.

## Experiment 1: varying |V| (p = 0.3)

| Vertices | Avg edges | Avg time (s) | time / ((V+E) log V) (ns) |
|---|---|---|---|
| 100 | 1485 | 0.000523 ± 0.000037 | 49.64 ± 3.39 |
| 200 | 5958 | 0.001342 ± 0.000074 | 28.51 ± 1.37 |
| 400 | 23928 | 0.003741 ± 0.000157 | 17.79 ± 0.79 |
| 800 | 95814 | 0.012059 ± 0.000787 | 12.94 ± 0.84 |

## Experiment 2: varying |E| (|V| = 1000)

| Edge prob. | Avg edges | Avg time (s) | time / ((V+E) log V) (ns) |
|---|---|---|---|
| 0.005 | 2495 | 0.004729 ± 0.000122 | 135.83 ± 4.69 |
| 0.01 | 4997 | 0.005450 ± 0.000122 | 91.23 ± 3.28 |
| 0.05 | 25078 | 0.007283 ± 0.000218 | 28.02 ± 0.86 |
| 0.1 | 50024 | 0.009419 ± 0.000277 | 18.52 ± 0.62 |
| 0.2 | 100023 | 0.013725 ± 0.000252 | 13.63 ± 0.24 |
| 0.4 | 199726 | 0.022795 ± 0.001269 | 11.39 ± 0.63 |
| 0.8 | 399696 | 0.045803 ± 0.009969 | 11.47 ± 2.50 |
