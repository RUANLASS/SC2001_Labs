"""
Tests for knapsack_bottom_up.py. Run with: python test_knapsack.py

The bottom-up algorithm is compared against
  (i)  a top-down memoised recursion implementing the Part 1 definition directly, and
  (ii) brute-force enumeration of item counts,
on random small instances, plus edge cases and the expected results of the brief.
"""
import itertools
import random
import sys

from knapsack_bottom_up import (INSTANCES, bottom_up_knapsack,
                                bottom_up_knapsack_trace)


def top_down(C, weights, profits):
    """Part 1 definition: P(C) = max({0} U {p_i + P(C - w_i) : w_i <= C}), memoised."""
    memo = {}

    def P(c):
        if c not in memo:
            memo[c] = max([0] + [profits[i] + P(c - weights[i])
                                 for i in range(len(weights)) if weights[i] <= c])
        return memo[c]

    return P(C)


def brute_force(C, weights, profits):
    """Try every combination of item counts whose total weight fits in C."""
    ranges = [range(C // w + 1) for w in weights]
    best = 0

    for counts in itertools.product(*ranges):
        if sum(k * w for k, w in zip(counts, weights)) <= C:
            best = max(best, sum(k * p for k, p in zip(counts, profits)))

    return best


def check_instance(C, weights, profits):
    """All implementations agree, and the traced solution is feasible and optimal."""
    fast = bottom_up_knapsack(C, weights, profits)
    trace = bottom_up_knapsack_trace(C, weights, profits)

    assert fast == trace["dp"][C]
    assert fast == top_down(C, weights, profits)
    assert fast == brute_force(C, weights, profits)

    # every entry of the DP array is P(c)
    for c in range(C + 1):
        assert trace["dp"][c] == top_down(c, weights, profits)

    # reconstructed items fit and reach the optimum
    counts = trace["counts"]
    assert sum(k * w for k, w in zip(counts, weights)) <= C
    assert sum(k * p for k, p in zip(counts, profits)) == fast


def test_random_instances():
    random.seed(42)

    for _ in range(300):
        n = random.randint(1, 4)
        C = random.randint(1, 25)
        weights = [random.randint(1, 10) for _ in range(n)]
        profits = [random.randint(1, 20) for _ in range(n)]
        check_instance(C, weights, profits)


def test_edge_cases():
    # C smaller than every weight
    assert bottom_up_knapsack(3, [4, 5, 8], [7, 6, 9]) == 0
    trace = bottom_up_knapsack_trace(3, [4, 5, 8], [7, 6, 9])
    assert trace["dp"] == [0, 0, 0, 0]
    assert trace["choice"] == [-1, -1, -1, -1]
    assert trace["counts"] == [0, 0, 0]

    # single item type
    assert bottom_up_knapsack(10, [3], [5]) == 15
    check_instance(10, [3], [5])

    # weight 1 (the knapsack can always be filled exactly)
    assert bottom_up_knapsack(7, [1, 4], [2, 9]) == top_down(7, [1, 4], [2, 9])
    check_instance(7, [1, 4], [2, 9])
    check_instance(9, [1], [3])

    # C equal to a weight
    check_instance(5, [5, 6], [4, 9])


def test_invalid_input():
    bad = [
        (10, [1, 2], [3]),          # different lengths
        (10, [0, 2], [3, 4]),       # zero weight
        (10, [1, 2], [3, -4]),      # negative profit
        (10, [1.5, 2], [3, 4]),     # non-integer weight
        (10, [True, 2], [3, 4]),    # bool is not accepted as an integer
        (0, [1, 2], [3, 4]),        # non-positive capacity
    ]

    for args in bad:
        for fn in (bottom_up_knapsack, bottom_up_knapsack_trace):
            try:
                fn(*args)
            except ValueError:
                continue
            raise AssertionError(f"{fn.__name__}{args} should raise ValueError")


def test_expected_results():
    # Instance (a): C = 16, w = [4, 5, 8], p = [7, 6, 9]
    a = INSTANCES["a"]
    trace = bottom_up_knapsack_trace(a["C"], a["weights"], a["profits"])
    assert trace["dp"] == [0, 0, 0, 0, 7, 7, 7, 7, 14, 14, 14, 14, 21, 21, 21, 21, 28]
    assert bottom_up_knapsack(16, a["weights"], a["profits"]) == 28
    assert trace["counts"] == [4, 0, 0]
    assert trace["candidates"][16] == [28, 20, 23]
    # same items as Part 2, whose graph used C = 15
    assert bottom_up_knapsack(15, a["weights"], a["profits"]) == 21

    # Instance (b): C = 12, w = [5, 6, 7], p = [7, 6, 9]
    b = INSTANCES["b"]
    trace = bottom_up_knapsack_trace(b["C"], b["weights"], b["profits"])
    assert trace["dp"] == [0, 0, 0, 0, 0, 7, 7, 9, 9, 9, 14, 14, 16]
    assert bottom_up_knapsack(12, b["weights"], b["profits"]) == 16
    assert trace["candidates"][12] == [16, 13, 16]
    # items 0 and 2 tie at c = 12; strict > keeps item 0 in choice[]
    assert trace["choice"][12] == 0
    # either way the multiset is one item 0 plus one item 2
    assert trace["counts"] == [1, 0, 1]


def main():
    tests = [test_random_instances, test_edge_cases, test_invalid_input, test_expected_results]

    for test in tests:
        test()
        print(f"PASS  {test.__name__}")

    print(f"All {len(tests)} test groups passed.")


if __name__ == "__main__":
    sys.exit(main())
