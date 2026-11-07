# SC2001 Project 3: Dynamic Programming

## Part 3: Bottom-Up Dynamic Programming Algorithm

### DP State

Let `DP[c]` represent the maximum total profit obtainable using a knapsack of capacity `c`.

This is equivalent to the recursive function defined in Part 1:

\[
DP[c] = P(c)
\]

### Base Case

When the knapsack has zero capacity, no objects can be packed:

\[
DP[0] = 0
\]

For any positive capacity where no object fits, the maximum profit is also zero. The algorithm handles this by initially setting `DP[c]` to zero before checking the object types.

### Recurrence Relation

For each capacity `c`, consider every object type `i` whose weight does not exceed `c`. If object `i` is selected, its profit is `p_i`, and the remaining capacity is `c - w_i`.

Therefore:

\[
DP[c] = \max\left(\{0\} \cup \{p_i + DP[c-w_i] : 0 \leq i < n,\ w_i \leq c\}\right)
\]

This is the same recurrence as Part 1, except that each smaller subproblem value is retrieved from the DP array instead of being calculated recursively.

### Bottom-Up Algorithm

```text
Algorithm BottomUpKnapsack(C, n, w, p):

    Create array DP[0...C]
    DP[0] <- 0

    For c <- 1 to C:

        DP[c] <- 0

        For i <- 0 to n-1:

            If w[i] <= c:

                candidate <- p[i] + DP[c - w[i]]

                If candidate > DP[c]:
                    DP[c] <- candidate

    Return DP[C]
```

The algorithm fills the DP array in increasing order of capacity. Therefore, whenever `DP[c]` is calculated, every required smaller-capacity value `DP[c - w[i]]` has already been computed and stored.

For each capacity, the algorithm checks every object type that can fit. The variable `candidate` stores the profit obtained by choosing the current object type together with the best solution for the remaining capacity. The algorithm updates `DP[c]` only when this candidate is greater than the best profit found so far.

Since object supplies are unlimited, the same object type may be selected again in the remaining-capacity subproblem.

### Correctness

We show that the algorithm computes the optimal profit for every capacity from `0` to `C`.

The base case is correct because a knapsack with capacity zero has maximum profit zero.

Assume that all DP entries for capacities smaller than `c` contain their optimal profits. For capacity `c`, any feasible non-empty packing contains at least one object of some type `i` with `w_i <= c`. Removing one such object leaves a knapsack of capacity `c - w_i`. By the optimal-substructure property from Part 1, the best possible profit for the remaining capacity is `DP[c - w_i]`. Thus, the best profit among solutions whose selected object is type `i` is `p_i + DP[c - w_i]`.

The algorithm checks every object type that fits and keeps the largest candidate, with zero as the initial value for the case where no object fits. Therefore, it obtains the optimal profit for capacity `c`.

By induction, every entry is computed correctly, including `DP[C]`, which is returned as the maximum profit.

### Complexity Analysis

- **Time complexity: \(O(nC)\).** The outer loop processes `C` capacities, and the inner loop checks up to `n` object types for each capacity.
- **Space complexity: \(O(C)\).** The algorithm stores `C + 1` values in the DP array, one for each capacity from `0` to `C`.
