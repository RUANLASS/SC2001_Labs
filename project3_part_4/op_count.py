"""
Deterministic check of the O(nC) claim (Part 3): count inner-loop iterations of the bottom-up
algorithm instead of timing it. Writes op_counts.csv and op_counts.png.
"""
import csv
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

ITEM_COUNTS = [1, 2, 4, 8, 16]
CAPACITIES = [100, 200, 400, 800, 1600, 3200]

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
LINE_COLOURS = ["#2a78d6", "#eb6834", "#2f9e58", "#8a5cd0", "#b8860b"]


def count_inner_iterations(C, weights, profits):
    """Run the Part 3 loops and count how often the inner loop body is entered."""
    n = len(weights)
    DP = [0] * (C + 1)
    iterations = 0

    for c in range(1, C + 1):
        DP[c] = 0

        for i in range(n):
            iterations += 1

            if weights[i] <= c:
                candidate = profits[i] + DP[c - weights[i]]

                if candidate > DP[c]:
                    DP[c] = candidate

    return iterations


def run_sweep():
    """Count iterations for every (n, C) pair on random items."""
    random.seed(42)
    rows = []

    for n in ITEM_COUNTS:
        for C in CAPACITIES:
            weights = [random.randint(1, 50) for _ in range(n)]
            profits = [random.randint(1, 100) for _ in range(n)]
            iterations = count_inner_iterations(C, weights, profits)
            rows.append({"n": n, "C": C, "inner_iterations": iterations,
                         "n_times_C": n * C, "equal": iterations == n * C})

    return rows


def plot(rows):
    fig, ax = plt.subplots(figsize=(8, 4.8), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=10)

    for colour, n in zip(LINE_COLOURS, ITEM_COUNTS):
        data = [r for r in rows if r["n"] == n]
        ax.plot([r["C"] for r in data], [r["inner_iterations"] for r in data], color=colour,
                linewidth=2, marker="o", markersize=6, markeredgecolor=SURFACE,
                markeredgewidth=1.5, label=f"n = {n}")

    ax.set_xlabel("Capacity C", color=TEXT_SECONDARY, fontsize=11)
    ax.set_ylabel("Inner-loop iterations", color=TEXT_SECONDARY, fontsize=11)
    ax.legend(frameon=False, fontsize=10, labelcolor=TEXT_PRIMARY, loc="upper left")

    fig.tight_layout()
    path = os.path.join(HERE, "op_counts.png")
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def main():
    rows = run_sweep()

    with open(os.path.join(HERE, "op_counts.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"{'n':>3} {'C':>5} {'iterations':>11} {'n*C':>7} equal")
    for r in rows:
        print(f"{r['n']:3} {r['C']:5} {r['inner_iterations']:11} {r['n_times_C']:7} {r['equal']}")

    mismatches = [r for r in rows if not r["equal"]]
    print(f"\n{len(rows) - len(mismatches)}/{len(rows)} cases have iterations == n*C exactly")
    plot(rows)


if __name__ == "__main__":
    main()
