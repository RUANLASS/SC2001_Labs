import os, csv
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

def read_csv(name):
    with open(os.path.join(RESULTS_DIR, name), newline="") as f:
        return list(csv.DictReader(f))

rows = read_csv("c2_comparisons_vs_S_10M_run.csv")
s_values = [int(r["S"]) for r in rows]
comparisons = [int(r["comparisons"]) for r in rows]
times = [float(r["cpu_time_s"]) for r in rows]
n_fixed = int(rows[0]["n"])

# comparisons vs S
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(s_values, comparisons, marker="o", color="#2563eb")
ax.set_xscale("log")
ax.set_xlabel("Threshold S (log scale)")
ax.set_ylabel("Comparisons")
ax.set_title(f"Comparisons vs S (n = {n_fixed:,}, fixed)")
ax.grid(True, which="both", linestyle=":", alpha=0.5)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS_DIR, "c2_comparisons_vs_S_10M.png"), dpi=150)
plt.close(fig)

# CPU time vs S
best_idx = min(range(len(times)), key=lambda i: times[i])
best_s, best_t = s_values[best_idx], times[best_idx]
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(s_values, times, marker="o", color="#2563eb")
ax.scatter([best_s], [best_t], color="#dc2626", zorder=5, s=80,
           label=f"Fastest: S={best_s} ({best_t:.4f}s)")
ax.set_xscale("log")
ax.set_xlabel("Threshold S (log scale)")
ax.set_ylabel("CPU time (s)")
ax.set_title(f"CPU time vs S (n = {n_fixed:,}, fixed)")
ax.legend()
ax.grid(True, which="both", linestyle=":", alpha=0.5)
fig.tight_layout()
fig.savefig(os.path.join(PLOTS_DIR, "c2_time_vs_S_10M.png"), dpi=150)
plt.close(fig)

print("wrote plots")
