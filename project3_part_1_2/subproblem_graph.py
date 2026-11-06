"""
Builds and draws the subproblem graph for P(15) in the unbounded knapsack
instance from the Project 3 brief: n = 3, weights = [4, 5, 8], profits = [7, 6, 9].

Node C represents the subproblem P(C). An edge C -> C - w_i exists whenever
item type i (weight w_i) fits in capacity C, since P(C) depends on P(C - w_i).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

weights = [4, 5, 8]
profits = [7, 6, 9]
TARGET = 15

# --- Discover every subproblem reachable from P(15), and every dependency edge ---
visited = {TARGET}
queue = [TARGET]
edges = []  # (from_C, to_C, item_index)
while queue:
    C = queue.pop(0)
    for i, w in enumerate(weights):
        if w <= C:
            nxt = C - w
            edges.append((C, nxt, i))
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)

nodes = sorted(visited, reverse=True)
print("Nodes (subproblems):", nodes)
print("Number of nodes:", len(nodes))
print("Number of edges:", len(edges))
for e in sorted(edges, key=lambda e: (-e[0], e[2])):
    print(f"  P({e[0]}) -> P({e[1]})  via item {e[2]} (w={weights[e[2]]}, p={profits[e[2]]})")

# --- Also compute P(C) for every node, bottom-up, to label each node with its value ---
Pval = {}
for C in sorted(visited):
    if C == 0:
        Pval[C] = 0
    else:
        best = 0
        for i, w in enumerate(weights):
            if w <= C:
                best = max(best, profits[i] + Pval[C - w])
        Pval[C] = best
print("P(C) values:", Pval)

# --- Draw: single horizontal row of nodes (descending C), arcs for edges ---
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#2f9e58"
item_colors = [BLUE, ORANGE, GREEN]

x = {C: idx for idx, C in enumerate(nodes)}  # left -> right = largest -> smallest
y0 = 0.0

fig, ax = plt.subplots(figsize=(12, 4.3))

# Edges as arcs above the line; curvature scaled by span so short/long edges don't collide
for (frm, to, i) in edges:
    x1, x2 = x[frm], x[to]
    span = x2 - x1  # negative (to is smaller C, further right)
    rad = 0.28 + 0.05 * abs(span)
    arrow = FancyArrowPatch(
        (x1, y0), (x2, y0),
        connectionstyle=f"arc3,rad={-0.18 - 0.03*abs(span)}",
        arrowstyle="-|>", mutation_scale=16,
        shrinkA=21, shrinkB=21,
        color=item_colors[i], linewidth=1.7, alpha=0.9, zorder=1,
    )
    ax.add_patch(arrow)

# Nodes
for C in nodes:
    ax.scatter([x[C]], [y0], s=1100, color="white", edgecolor="#1a1a1a", linewidth=1.6, zorder=3)
    ax.text(x[C], y0, f"P({C})", ha="center", va="center", fontsize=11, fontweight="bold", zorder=4)
    ax.text(x[C], y0 - 0.55, f"= {Pval[C]}", ha="center", va="center", fontsize=9.5, color="#555555", zorder=4)

# Legend for item colors
handles = [
    plt.Line2D([0], [0], color=item_colors[i], lw=2.2,
               label=f"item {i}  (w={weights[i]}, p={profits[i]})")
    for i in range(len(weights))
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02),
          ncol=3, frameon=False, fontsize=10)

ax.set_xlim(-0.8, len(nodes) - 0.2)
ax.set_ylim(-1.35, 2.25)
ax.axis("off")
ax.set_title("Subproblem graph for P(15)  —  n = 3, w = [4, 5, 8], p = [7, 6, 9]",
             fontsize=13, fontweight="bold", pad=14)

plt.tight_layout()
plt.savefig("subproblem_graph.png", dpi=200, bbox_inches="tight")
print("Saved subproblem_graph.png")
