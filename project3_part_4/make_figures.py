"""
Generates the Part 4 slide figures from slide_data.json (written by run_part4.py):
dp_bars_a.png, dp_bars_b.png, final_cell_a.png, final_cell_b.png.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_JSON = os.path.join(HERE, "slide_data.json")

# House palette: item colours match project3_part_1_2/subproblem_graph.py
ITEM_COLOURS = ["#2a78d6", "#eb6834", "#2f9e58"]
NO_ITEM_COLOUR = "#c9c8c2"
SURFACE = "#fcfcfb"

TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"

FONT = 12
FIGSIZE = (10, 5.625)  # 16:9
DPI = 200


def load_data():
    with open(DATA_JSON) as f:
        return json.load(f)


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    # profits are integers, so use integer ticks only
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=FONT)
    ax.xaxis.label.set_color(TEXT_SECONDARY)
    ax.yaxis.label.set_color(TEXT_SECONDARY)
    ax.xaxis.label.set_size(FONT)
    ax.yaxis.label.set_size(FONT)


def item_label(data, i):
    return f"item {i} (w={data['weights'][i]}, p={data['profits'][i]})"


def save(fig, name):
    path = os.path.join(HERE, name)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def plot_dp_bars(name, data):
    """DP[c] against c, coloured by the item chosen at that capacity."""
    C, dp, choice = data["C"], data["dp"], data["choice"]
    colours = [NO_ITEM_COLOUR if k == -1 else ITEM_COLOURS[k] for k in choice]

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor=SURFACE)
    style_axes(ax)
    bars = ax.bar(range(C + 1), dp, color=colours, width=0.8)

    # highlight the final bar
    bars[C].set_edgecolor(TEXT_PRIMARY)
    bars[C].set_linewidth(2.5)

    # value labels; the final bar gets the P(C) annotation instead
    for c in range(C):
        ax.annotate(str(dp[c]), (c, dp[c]), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=FONT, color=TEXT_SECONDARY)
    ax.annotate(f"P({C}) = {dp[C]}", (C, dp[C]), xytext=(0, 5), textcoords="offset points",
                ha="center", fontsize=FONT, fontweight="bold", color=TEXT_PRIMARY)

    # legend: every item, plus the capacities where no item fits (DP = 0)
    handles = []
    for i in range(len(data["weights"])):
        label = item_label(data, i)
        if i not in choice:
            label += " - never chosen"
        handles.append(Patch(facecolor=ITEM_COLOURS[i], label=label))
    if -1 in choice:
        handles.append(Patch(facecolor=NO_ITEM_COLOUR, label="no item gives profit (DP = 0)"))

    ax.set_xticks(range(C + 1))
    ax.set_xlim(-0.8, C + 0.8)
    ax.set_ylim(0, max(dp) * 1.18)
    ax.set_xlabel("Capacity c")
    ax.set_ylabel("DP[c] = P(c)  (maximum profit)")
    ax.legend(handles=handles, title="Item chosen at capacity c", frameon=False,
              fontsize=FONT, title_fontsize=FONT, labelcolor=TEXT_PRIMARY, loc="upper left")
    ax.get_legend().get_title().set_color(TEXT_PRIMARY)

    save(fig, f"dp_bars_{name}.png")


def plot_final_cell(name, data):
    """The final capacity's candidates side by side, with the maximum highlighted."""
    C, dp = data["C"], data["dp"]
    weights, profits = data["weights"], data["profits"]
    cands = data["final_candidates"]
    best = dp[C]

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor=SURFACE)
    style_axes(ax)

    tick_labels = []
    for cand in cands:
        i = cand["item"]
        head = f"item {i}\n(w={weights[i]}, p={profits[i]})"
        if cand["fits"]:
            rest = C - weights[i]
            tick_labels.append(f"{head}\n{profits[i]} + DP[{rest}]\n= {profits[i]} + {dp[rest]}")
        else:
            tick_labels.append(f"{head}\ndoes not fit")

    for cand in cands:
        i = cand["item"]
        if not cand["fits"]:
            ax.text(i, best * 0.02, "does not fit", ha="center", va="bottom",
                    fontsize=FONT, color=TEXT_SECONDARY)
            continue

        is_best = cand["candidate"] == best
        bar = ax.bar(i, cand["candidate"], color=ITEM_COLOURS[i], width=0.55,
                     edgecolor=TEXT_PRIMARY if is_best else SURFACE,
                     linewidth=3 if is_best else 0)
        text = f"{cand['candidate']}" + ("  (maximum)" if is_best else "")
        ax.annotate(text, (i, cand["candidate"]), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=FONT, color=TEXT_PRIMARY,
                    fontweight="bold" if is_best else "normal")

    ax.set_xticks(range(len(cands)))
    ax.set_xticklabels(tick_labels)
    ax.set_xlim(-0.6, len(cands) - 0.4)
    ax.set_ylim(0, best * 1.18)
    ax.set_xlabel(f"Item type tried at capacity c = {C}")
    ax.set_ylabel("Candidate  p_i + DP[c - w_i]")

    handles = [Patch(facecolor=SURFACE, edgecolor=TEXT_PRIMARY, linewidth=2.5,
                     label=f"maximum candidate = DP[{C}] = {best}")]
    ax.legend(handles=handles, frameon=False, fontsize=FONT, labelcolor=TEXT_PRIMARY,
              loc="upper right")

    save(fig, f"final_cell_{name}.png")


def main():
    data = load_data()

    for name in ["a", "b"]:
        plot_dp_bars(name, data[name])
        plot_final_cell(name, data[name])


if __name__ == "__main__":
    main()
