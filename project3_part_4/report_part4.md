# SC2001 Project 3: Dynamic Programming

## Part 4: Implementation and Running Results

### How to Run

All commands are run from the `project3_part_4/` folder (Python 3; `make_figures.py` and `op_count.py` also need matplotlib).

```text
python test_knapsack.py   # checks the algorithm against the Part 1 recursion and brute force
python run_part4.py       # prints the running results, writes run_output.txt, slide_data.json, dp_instance_*.csv
python make_figures.py    # slide figures from slide_data.json
python op_count.py        # optional: inner-loop iteration counts (op_counts.csv, op_counts.png)
```

`knapsack_bottom_up.py` contains `bottom_up_knapsack`, a direct translation of the Part 3 pseudocode, and `bottom_up_knapsack_trace`, which runs the same loops but also records the item chosen at each capacity so that the packed items can be reconstructed. The two functions give identical DP values.

### Running Result of P(16)

Items from Part 2: `C = 16`, `w = [4, 5, 8]`, `p = [7, 6, 9]`.

```text
c      0  1  2  3  4  5  6  7  8   9  10  11  12  13  14  15  16
DP[c]  0  0  0  0  7  7  7  7  14  14  14  14  21  21  21  21  28
```

Candidates for the final capacity `c = 16`:

| Item | Weight | Profit | `p_i + DP[16 - w_i]` |
|---:|---:|---:|---:|
| 0 | 4 | 7 | 7 + DP[12] = 28 |
| 1 | 5 | 6 | 6 + DP[11] = 20 |
| 2 | 8 | 9 | 9 + DP[8] = 23 |

Maximum profit: **P(16) = 28**, obtained from four copies of item 0 (total weight 16).

### Running Result of P(12)

Items: `C = 12`, `w = [5, 6, 7]`, `p = [7, 6, 9]`.

```text
c      0  1  2  3  4  5  6  7  8  9  10  11  12
DP[c]  0  0  0  0  0  7  7  9  9  9  14  14  16
```

Candidates for the final capacity `c = 12`:

| Item | Weight | Profit | `p_i + DP[12 - w_i]` |
|---:|---:|---:|---:|
| 0 | 5 | 7 | 7 + DP[7] = 16 |
| 1 | 6 | 6 | 6 + DP[6] = 13 |
| 2 | 7 | 9 | 9 + DP[5] = 16 |

Maximum profit: **P(12) = 16**, obtained from one copy of item 0 and one copy of item 2 (total weight 12). Items 0 and 2 tie at `c = 12`; because the update uses a strict `>`, `choice[12]` keeps item 0, and the reconstructed set is the same either way.

The full console output is in `run_output.txt`.

### Interpretation

For the first instance, the item with the best profit per unit weight (item 0, 7/4) divides the capacity exactly, so `DP` rises in steps of 7 every 4 units and the optimum is simply four copies of item 0; the larger items are never chosen. Because the same item may be used repeatedly, `P(15) = 21` is also visible in the table, matching the Part 2 graph. In the second instance no single item dominates: item 2 is the best choice at capacities 7 to 9, but at capacity 12 the best packing mixes item 0 (weight 5) and item 2 (weight 7), which fill the knapsack exactly. Item 1 never gives the best candidate in either instance.
