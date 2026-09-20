"""
Member B -- (c)(ii) rerun at n = 10,000,000, run in chunks (foreground, per-call).
Usage: python3 experiment_c2_10M.py S1 S2 S3 ...
Appends rows to results/c2_comparisons_vs_S_10M_run.csv
"""
import os, sys, csv, time, copy
from hybrid_sort import hybrid_merge_insertion_sort
from generate_data import generate_dataset

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
PATH = os.path.join(RESULTS_DIR, "c2_comparisons_vs_S_10M_run.csv")

N_FIXED = 10_000_000

def timed_hybrid(arr, s):
    a = copy.deepcopy(arr)
    t0 = time.process_time()
    sorted_a, comparisons = hybrid_merge_insertion_sort(a, s)
    t1 = time.process_time()
    assert sorted_a == sorted(arr), "incorrect sort result!"
    return comparisons, t1 - t0

def main():
    s_values = [int(x) for x in sys.argv[1:]]
    new_file = not os.path.exists(PATH)
    f = open(PATH, "a", newline="")
    w = csv.writer(f)
    if new_file:
        w.writerow(["n", "S", "comparisons", "cpu_time_s"])
    arr = generate_dataset(N_FIXED, seed=2024)
    for s in s_values:
        c, t = timed_hybrid(arr, s)
        w.writerow([N_FIXED, s, c, f"{t:.6f}"])
        f.flush()
        print(f"[c2-10M] n={N_FIXED} S={s:>4d} comparisons={c:>12d} time={t:.4f}s", flush=True)
    f.close()
    print("CHUNK DONE", flush=True)

if __name__ == "__main__":
    main()
