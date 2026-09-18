# Part (c): Growth Analysis — Comparisons vs n and vs S

## (c)(i) Comparisons vs n, fixed S

With S fixed at 16, comparisons were measured for n ranging from 1,000 to
10,000,000 ([results/c1_comparisons_vs_n.csv](results/c1_comparisons_vs_n.csv),
plotted in [plots/c1_comparisons_vs_n.png](plots/c1_comparisons_vs_n.png)).
On the log-log plot, the measured curve sits almost exactly on top of the
theoretical n·log₂(n) reference curve (scaled to match at n = 10,000,000)
across the entire four-decade range of n. This matches the earlier
complexity analysis: for fixed S, the hybrid sort does O(n·S) work in the
insertion-sort base cases (a constant factor times n, since S is fixed) and
O(n·log(n/S)) work in the merge stage, and the log(n/S) term is what gives
the curve its n·log(n) shape once S is held constant. The close fit confirms
that, at a fixed threshold, the algorithm's real comparison count grows at
the same rate as the O(n log n) bound predicts, with no visible drift at
either end of the range.

## (c)(ii) Comparisons vs S, fixed n

With n fixed at 1,000,000, comparisons were measured for S ranging from 1 to
256 ([results/c2_comparisons_vs_S.csv](results/c2_comparisons_vs_S.csv),
plotted in [plots/c2_comparisons_vs_S.png](plots/c2_comparisons_vs_S.png)).
Comparisons rise monotonically with S — there is no interior minimum. This
is expected: increasing S shrinks the merge stage's log(n/S) depth, but that
saving is only logarithmic, while each insertion-sort base case grows
quadratically in cost (O(S²) comparisons per block, over n/S blocks, giving
O(n·S) total). Since O(S) grows strictly faster than O(log(n/S)) shrinks as
S increases, the trade-off never favors a larger S in terms of raw
comparison count — the curve should decrease only if the O(S²) term could
ever beat merge's O(log S) savings, and it can't, so the minimum comparison
count sits at the smallest S tested (S = 1, which reduces to plain merge
sort).

The companion CPU-time plot
([plots/c2_time_vs_S.png](plots/c2_time_vs_S.png)) tells a slightly
different story from raw comparisons: measured time is flattest — and
actually lowest — around S ≈ 8–24 (fastest at S = 12, 1.51s), rising sharply
above S ≈ 100. This is a constant-factor effect specific to this Python
implementation rather than a change in the comparison-count trend: very
small S values (S = 1–2) incur relatively more Python function-call/recursion
overhead per element from deeply nested merge calls, while very large S
values (S ≥ 128) start paying the O(S²) insertion-sort cost in wall-clock
time, not just in comparisons. So although comparisons alone never have an
interior minimum, wall-clock time can, purely from implementation overhead —
a distinction worth keeping in mind when choosing S in practice versus when
proving asymptotic bounds.
