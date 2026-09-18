"""
Member B -- Growth Analysis plots
Assignment parts covered: (c)(i) comparisons vs n (fixed S), (c)(ii) comparisons vs S (fixed n)

Reads results/c1_comparisons_vs_n.csv and results/c2_comparisons_vs_S.csv
(written by experiment_b.py) and produces:
  plots/c1_comparisons_vs_n.png
  plots/c2_comparisons_vs_S.png
  plots/c2_time_vs_S.png

Run: python3 plot_results.py
"""
import os
import csv
import math

import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def read_csv(name):
    path = os.path.join(RESULTS_DIR, name)
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------
# (c)(i): comparisons vs n, fixed S -- log-log with n*log2(n) reference
# ---------------------------------------------------------------------
def plot_c1():
    rows = read_csv("c1_comparisons_vs_n.csv")
    ns = [int(r["n"]) for r in rows]
    comparisons = [int(r["comparisons"]) for r in rows]
    s_fixed = rows[0]["S"]

    # theoretical n*log2(n) curve, scaled to match actual data at the largest n
    n_log_n = [n * math.log2(n) for n in ns]
    scale = comparisons[-1] / n_log_n[-1]
    theory = [scale * v for v in n_log_n]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, comparisons, marker="o", label="Measured comparisons", color="#2563eb")
    ax.plot(ns, theory, linestyle="--", label=r"$n\log_2 n$ (scaled to match at largest $n$)", color="#f97316")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Input size n (log scale)")
    ax.set_ylabel("Comparisons (log scale)")
    ax.set_title(f"Comparisons vs n (S = {s_fixed}, fixed)")
    ax.legend()
    ax.grid(True, which="both", linestyle=":", alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "c1_comparisons_vs_n.png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------
# (c)(ii): comparisons vs S, fixed n
# ---------------------------------------------------------------------
def plot_c2_comparisons():
    rows = read_csv("c2_comparisons_vs_S.csv")
    s_values = [int(r["S"]) for r in rows]
    comparisons = [int(r["comparisons"]) for r in rows]
    n_fixed = rows[0]["n"]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(s_values, comparisons, marker="o", color="#2563eb")

    ax.set_xscale("log")
    ax.set_xlabel("Threshold S (log scale)")
    ax.set_ylabel("Comparisons")
    ax.set_title(f"Comparisons vs S (n = {int(n_fixed):,}, fixed)")
    ax.grid(True, which="both", linestyle=":", alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "c2_comparisons_vs_S.png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------
# (c)(ii) companion: CPU time vs S, fixed n -- marks the fastest S
# ---------------------------------------------------------------------
def plot_c2_time():
    rows = read_csv("c2_comparisons_vs_S.csv")
    s_values = [int(r["S"]) for r in rows]
    times = [float(r["cpu_time_s"]) for r in rows]
    n_fixed = rows[0]["n"]

    best_idx = min(range(len(times)), key=lambda i: times[i])
    best_s, best_t = s_values[best_idx], times[best_idx]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(s_values, times, marker="o", color="#2563eb")
    ax.scatter([best_s], [best_t], color="#dc2626", zorder=5, s=80,
               label=f"Fastest: S={best_s} ({best_t:.4f}s)")

    ax.set_xscale("log")
    ax.set_xlabel("Threshold S (log scale)")
    ax.set_ylabel("CPU time (s)")
    ax.set_title(f"CPU time vs S (n = {int(n_fixed):,}, fixed)")
    ax.legend()
    ax.grid(True, which="both", linestyle=":", alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "c2_time_vs_S.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    plot_c1()
    plot_c2_comparisons()
    plot_c2_time()
    print("Wrote plots to", PLOTS_DIR)
