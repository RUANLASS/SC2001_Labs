"""
Bottom-up dynamic programming for the unbounded knapsack problem (Project 3, Part 4).

DP[c] is the maximum total profit obtainable with a knapsack of capacity c, i.e. P(c)
from Part 1. The algorithm is the Part 3 pseudocode (bottom_up_pseudocode.txt):
O(nC) time, O(C) space.
"""


def validate(C, weights, profits):
    """Raise ValueError unless the instance is well formed."""
    if len(weights) != len(profits):
        raise ValueError("weights and profits must have the same length")

    # bool is a subclass of int, so reject it explicitly
    for value in [C] + list(weights) + list(profits):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"all values must be positive integers, got {value!r}")


def bottom_up_knapsack(C, weights, profits):
    """Return the maximum profit DP[C] (line-by-line translation of the Part 3 pseudocode)."""
    validate(C, weights, profits)
    n = len(weights)

    # Create array DP[0...C]
    DP = [0] * (C + 1)
    # DP[0] <- 0
    DP[0] = 0

    # For c <- 1 to C
    for c in range(1, C + 1):
        # DP[c] <- 0
        DP[c] = 0

        # For i <- 0 to n-1
        for i in range(n):
            # If w[i] <= c
            if weights[i] <= c:
                candidate = profits[i] + DP[c - weights[i]]

                # Update only when the candidate is strictly greater
                if candidate > DP[c]:
                    DP[c] = candidate

    return DP[C]


def bottom_up_knapsack_trace(C, weights, profits):
    """Same loops as bottom_up_knapsack, but also record how every DP[c] was obtained.

    Returns a dict with:
      dp          the full DP array (DP[0..C])
      choice      choice[c] = item index that achieved DP[c], -1 if no item fits / helps.
                  Ties go to the lowest index because the update is strict >.
      candidates  candidates[c][i] = p_i + DP[c - w_i], or None if item i does not fit
      counts      counts[i] = copies of item i in the reconstructed solution for capacity C
    """
    validate(C, weights, profits)
    n = len(weights)

    DP = [0] * (C + 1)
    choice = [-1] * (C + 1)
    candidates = [[None] * n for _ in range(C + 1)]

    for c in range(1, C + 1):
        DP[c] = 0

        for i in range(n):
            if weights[i] <= c:
                candidate = profits[i] + DP[c - weights[i]]
                candidates[c][i] = candidate

                if candidate > DP[c]:
                    DP[c] = candidate
                    choice[c] = i

    return {
        "dp": DP,
        "choice": choice,
        "candidates": candidates,
        "counts": reconstruct_counts(C, weights, choice),
    }


def reconstruct_counts(C, weights, choice):
    """Walk choice[] from capacity C to count how many copies of each item are used."""
    counts = [0] * len(weights)
    c = C

    # choice[c] == -1 means DP[c] = 0, so nothing more is packed
    while c > 0 and choice[c] != -1:
        counts[choice[c]] += 1
        c -= weights[choice[c]]

    return counts


# The two instances of the Part 4 brief
INSTANCES = {
    "a": {"C": 16, "weights": [4, 5, 8], "profits": [7, 6, 9]},
    "b": {"C": 12, "weights": [5, 6, 7], "profits": [7, 6, 9]},
}


def main():
    for name, inst in INSTANCES.items():
        result = bottom_up_knapsack(inst["C"], inst["weights"], inst["profits"])
        trace = bottom_up_knapsack_trace(inst["C"], inst["weights"], inst["profits"])
        print(f"Instance ({name}): C = {inst['C']}, w = {inst['weights']}, p = {inst['profits']}")
        print(f"  P({inst['C']}) = {result}   items used: {trace['counts']}")


if __name__ == "__main__":
    main()
