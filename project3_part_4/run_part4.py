"""
Runs both Part 4 instances, prints the running results and writes the files used by the slides:
run_output.txt, slide_data.json, dp_instance_a.csv and dp_instance_b.csv.
"""
import csv
import json
import os

from knapsack_bottom_up import (INSTANCES, bottom_up_knapsack,
                                bottom_up_knapsack_trace)

HERE = os.path.dirname(os.path.abspath(__file__))


def solve(inst):
    """Run both implementations on an instance and collect everything worth reporting."""
    C, weights, profits = inst["C"], inst["weights"], inst["profits"]
    trace = bottom_up_knapsack_trace(C, weights, profits)

    # the plain and traced versions must agree
    assert bottom_up_knapsack(C, weights, profits) == trace["dp"][C]

    counts = trace["counts"]
    final_candidates = [
        {"item": i, "fits": trace["candidates"][C][i] is not None,
         "candidate": trace["candidates"][C][i]}
        for i in range(len(weights))
    ]

    return {
        "C": C,
        "weights": weights,
        "profits": profits,
        "dp": trace["dp"],
        "choice": trace["choice"],
        "candidates": trace["candidates"],
        "item_counts": counts,
        "total_weight": sum(k * w for k, w in zip(counts, weights)),
        "total_profit": sum(k * p for k, p in zip(counts, profits)),
        "final_candidates": final_candidates,
    }


def describe(name, result):
    """Return the console output for one instance as a list of lines."""
    C, weights, profits = result["C"], result["weights"], result["profits"]
    dp, choice = result["dp"], result["choice"]
    lines = []

    lines.append("=" * 60)
    lines.append(f"Instance ({name}): C = {C}, n = {len(weights)}, w = {weights}, p = {profits}")
    lines.append("=" * 60)

    lines.append("")
    lines.append("DP table (choice = item achieving DP[c], -1 = none):")
    lines.append("  c | DP[c] | choice")
    for c in range(C + 1):
        lines.append(f"{c:3} | {dp[c]:5} | {choice[c]:6}")

    lines.append("")
    lines.append(f"Candidates for the final capacity c = {C}:")
    for cand in result["final_candidates"]:
        i = cand["item"]
        if cand["fits"]:
            lines.append(f"  item {i} (w={weights[i]}, p={profits[i]}): fits, "
                         f"p + DP[{C - weights[i]}] = {profits[i]} + {dp[C - weights[i]]} "
                         f"= {cand['candidate']}")
        else:
            lines.append(f"  item {i} (w={weights[i]}, p={profits[i]}): does not fit "
                         f"(w > {C})")

    best = [c["item"] for c in result["final_candidates"] if c["fits"] and c["candidate"] == dp[C]]
    if len(best) > 1:
        lines.append(f"  items {best} tie for the maximum; strict > keeps item {choice[C]} in choice[{C}]")

    lines.append("")
    lines.append(f"Maximum profit P({C}) = {dp[C]}")
    lines.append("Chosen items:")
    for i, k in enumerate(result["item_counts"]):
        if k > 0:
            lines.append(f"  item {i} (w={weights[i]}, p={profits[i]}) x {k}")
    lines.append(f"Total weight = {result['total_weight']} (capacity {C})")
    lines.append(f"Total profit = {result['total_profit']}")
    lines.append("")

    return lines


def write_csv(name, result):
    """One row per capacity: c, DP, choice and the candidate of every item (blank if not fitting)."""
    n = len(result["weights"])
    path = os.path.join(HERE, f"dp_instance_{name}.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["c", "DP", "choice"] + [f"candidate_item{i}" for i in range(n)])
        for c, value in enumerate(result["dp"]):
            row = ["" if x is None else x for x in result["candidates"][c]]
            writer.writerow([c, value, result["choice"][c]] + row)


def main():
    lines = []
    slide_data = {}

    for name, inst in INSTANCES.items():
        result = solve(inst)
        lines += describe(name, result)
        write_csv(name, result)

        # the per-capacity candidate table lives in the CSV; the JSON keeps the slide fields
        slide_data[name] = {k: v for k, v in result.items() if k != "candidates"}

    output = "\n".join(lines)
    print(output)

    with open(os.path.join(HERE, "run_output.txt"), "w") as f:
        f.write(output + "\n")

    with open(os.path.join(HERE, "slide_data.json"), "w") as f:
        json.dump(slide_data, f, indent=2)


if __name__ == "__main__":
    main()
