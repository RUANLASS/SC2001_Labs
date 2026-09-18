"""
Member B -- Growth Analysis
Assignment parts covered: (c)(i) comparisons vs n (fixed S), (c)(ii) comparisons vs S (fixed n)

Uses the team's actual shared code:
  - hybrid_sort.py   -> hybrid_merge_insertion_sort(arr, s) -> (sorted_arr, comparisons)
  - generate_data.py -> generate_dataset(size, x=DEFAULT_X, seed=None) -> list[int]

Run: python3 experiment_b.py
Writes results/*.csv and plots/*.png
"""
import os
import csv
import time
import copy

from hybrid_sort import hybrid_merge_insertion_sort
from generate_data import generate_dataset

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


def open_csv(name, header):
    path = os.path.join(RESULTS_DIR, name)
    f = open(path, "w", newline="")
    w = csv.writer(f)
    w.writerow(header)
    return f, w


def timed_hybrid(arr, s):
    a = copy.deepcopy(arr)
    t0 = time.process_time()
    sorted_a, comparisons = hybrid_merge_insertion_sort(a, s)
    t1 = time.process_time()
    assert sorted_a == sorted(arr), "hybrid_merge_insertion_sort produced an incorrect result!"
    return comparisons, t1 - t0


# ---------------------------------------------------------------------
# (c)(i): fixed S, vary n
# ---------------------------------------------------------------------
def experiment_c1(S_FIXED=16):
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000,
             500000, 1000000, 2000000, 5000000, 10000000]
    f, w = open_csv("c1_comparisons_vs_n.csv", ["n", "S", "comparisons", "cpu_time_s"])
    for n in sizes:
        arr = generate_dataset(n, seed=1000 + n)
        c, t = timed_hybrid(arr, S_FIXED)
        w.writerow([n, S_FIXED, c, f"{t:.6f}"])
        f.flush()
        print(f"[c1] n={n:>9d} S={S_FIXED} comparisons={c:>12d} time={t:.4f}s", flush=True)
    f.close()


# ---------------------------------------------------------------------
# (c)(ii): fixed n, vary S
# ---------------------------------------------------------------------
def experiment_c2(N_FIXED=1000000):
    s_values = [1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256]
    arr = generate_dataset(N_FIXED, seed=2024)
    f, w = open_csv("c2_comparisons_vs_S.csv", ["n", "S", "comparisons", "cpu_time_s"])
    for s in s_values:
        c, t = timed_hybrid(arr, s)
        w.writerow([N_FIXED, s, c, f"{t:.6f}"])
        f.flush()
        print(f"[c2] n={N_FIXED} S={s:>4d} comparisons={c:>12d} time={t:.4f}s", flush=True)
    f.close()


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "c1"):
        experiment_c1()
    if which in ("all", "c2"):
        experiment_c2()
    print("DONE", which, flush=True)
