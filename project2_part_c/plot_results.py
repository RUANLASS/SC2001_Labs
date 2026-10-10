
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_CSV = os.path.join(HERE, "results.csv")

# Colours: (a) array = blue, (b) heap = orange; text stays in neutral ink
ARRAY_COLOUR = "#2a78d6"
HEAP_COLOUR = "#eb6834"
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"

ARRAY_LABEL = "(a) adjacency matrix + array"
HEAP_LABEL = "(b) adjacency lists + min-heap"


def load_rows():
    with open(RESULTS_CSV) as f:
        return list(csv.DictReader(f))


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=9)
    ax.xaxis.label.set_color(TEXT_SECONDARY)
    ax.yaxis.label.set_color(TEXT_SECONDARY)
    ax.title.set_color(TEXT_PRIMARY)


def plot_series(ax, x, array_times, heap_times):
    ax.plot(x, array_times, color=ARRAY_COLOUR, linewidth=2, marker="o", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=1.5, label=ARRAY_LABEL)
    ax.plot(x, heap_times, color=HEAP_COLOUR, linewidth=2, marker="s", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=1.5, label=HEAP_LABEL)


def label_end(ax, x, y, text):
    ax.annotate(text, (x, y), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9, color=TEXT_PRIMARY)


def plot_time_vs_density(rows):
    data = [r for r in rows if r["experiment"] == "vary_density"]
    p = [float(r["edge_probability"]) for r in data]
    array_times = [float(r["array_time_s"]) * 1000 for r in data]
    heap_times = [float(r["heap_time_s"]) * 1000 for r in data]

    fig, ax = plt.subplots(figsize=(8, 4.8), facecolor=SURFACE)
    style_axes(ax)
    plot_series(ax, p, array_times, heap_times)
    label_end(ax, p[-1], array_times[-1], "(a)")
    label_end(ax, p[-1], heap_times[-1], "(b)")

    ax.set_xlim(0, 1.08)
    ax.set_ylim(0, max(array_times) * 1.15)
    ax.set_xlabel("Edge probability p   (|E| ≈ p · |V|(|V|−1)/2)")
    ax.set_ylabel("Average execution time (ms)")
    ax.set_title("Random graphs, |V| = 1000: execution time vs. edge density",
                 loc="left", fontsize=11)
    ax.legend(frameon=False, fontsize=9, labelcolor=TEXT_PRIMARY, loc="lower right")

    fig.tight_layout()
    path = os.path.join(HERE, "time_vs_density.png")
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def plot_time_vs_vertices(rows):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True, facecolor=SURFACE)
    panels = [
        ("vary_vertices", "Random graphs, p = 0.3"),
        ("worst_case", "Worst-case complete graphs\n(every edge triggers a heap update)"),
    ]

    for ax, (experiment, title) in zip(axes, panels):
        data = [r for r in rows if r["experiment"] == experiment]
        n = [int(r["vertices"]) for r in data]
        array_times = [float(r["array_time_s"]) * 1000 for r in data]
        heap_times = [float(r["heap_time_s"]) * 1000 for r in data]

        style_axes(ax)
        plot_series(ax, n, array_times, heap_times)
        label_end(ax, n[-1], array_times[-1], "(a)")
        label_end(ax, n[-1], heap_times[-1], "(b)")

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(n)
        ax.set_xticklabels([str(v) for v in n])
        ax.minorticks_off()
        ax.set_xlim(n[0] * 0.8, n[-1] * 1.5)
        ax.set_xlabel("Number of vertices |V| (log scale)")
        ax.set_title(title, loc="left", fontsize=11)

    axes[0].set_ylabel("Average execution time (ms, log scale)")
    axes[0].legend(frameon=False, fontsize=9, labelcolor=TEXT_PRIMARY, loc="upper left")

    fig.tight_layout()
    path = os.path.join(HERE, "time_vs_vertices.png")
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def main():
    rows = load_rows()
    plot_time_vs_density(rows)
    plot_time_vs_vertices(rows)


if __name__ == "__main__":
    main()
