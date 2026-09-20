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

## (c)(ii) rerun at n = 10,000,000 (matching part (d)'s input size)

To keep every part of the analysis on the same input size, (c)(ii) was
rerun with n fixed at 10,000,000 instead of 1,000,000, using the same S
values as the team's (c)(iii) sweep (1, 5, 10, 15, 20, 25, 30, 40, 50)
([results/c2_comparisons_vs_S_10M_run.csv](results/c2_comparisons_vs_S_10M_run.csv),
plots in
[plots/c2_comparisons_vs_S_10M.png](plots/c2_comparisons_vs_S_10M.png) and
[plots/c2_time_vs_S_10M.png](plots/c2_time_vs_S_10M.png)).

The comparisons-vs-S result is unchanged in shape: still monotonically
increasing with S, confirming the same O(n·S) vs O(n·log(n/S)) trade-off
holds regardless of n.

The CPU-time result is where it gets interesting. On this run, the fastest
S was 30 (25.21s), with S = 10, 15, and 30 all clustered within about 0.6s
of each other (25.2s–25.8s) — meaningfully flatter than a single sharp
minimum. That's a different "optimal S" than earlier independent checks by
other team members at the same n (S = 5 and S = 10 were both found fastest
on different machines). The most likely explanation is a combination of
run-to-run timing noise and genuine cross-machine differences — the
absolute CPU times measured here (25–29s) were roughly half of what was
measured on another team member's machine for the identical (n, S)
configuration, which points to hardware differences rather than a bug.

The honest conclusion: at n = 10,000,000, S in roughly the 5–30 range all
perform near-optimally in CPU time, and pinning down one single "best" S
more precisely than that would require averaging multiple runs on the same
machine — raw comparison count, by contrast, is deterministic and doesn't
have this problem.

## (c)(iii) determining the Optimal Threshold S

To determine a suitable threshold S for the hybrid Merge Sort algorithm, experiments were conducted using different input sizes ranging from 10,000 to 10,000,000 integers. For each input size, several values of S were tested. The same generated dataset was used for all S values at a given input size to ensure a fair comparison. Each configuration was run three times, and the average CPU time was recorded. For the 10,000,000-element dataset, the tested threshold values were S = 1, 5, 10, 15, 20, 25, 30, 40, and 50. The lowest average CPU time was obtained at S=15, with an average CPU time of approximately 45.73 seconds. Although some smaller threshold values resulted in fewer key comparisons, they did not necessarily result in lower CPU time. This demonstrates that the number of key comparisons alone does not fully determine the execution time of the algorithm, as other factors such as recursion and merging overhead also affect performance. Therefore, based on the tested values, S=15 was selected as the threshold for the 10,000,000-element dataset and used in Part (d). This threshold should be understood as the best-performing value among the tested values for this particular experimental setup, rather than a universally optimal threshold.

## (d) comparison of Original Merge Sort and Hybrid Merge+Insertion Sort

The original Merge Sort and the hybrid Merge+Insertion Sort were compared using the same dataset containing 10,000,000 integers. The hybrid algorithm used the threshold S=15 selected from Part (c)(iii). Both algorithms were run three times, and their average CPU times were recorded. The number of key comparisons was also measured. The original Merge Sort performed 220,099,725 key comparisons and required an average CPU time of approximately 74.04 seconds. In comparison, the hybrid Merge+Insertion Sort performed 226,417,560 key comparisons, which is approximately 2.87% more than the original Merge Sort. However, the hybrid algorithm recorded a substantially lower average CPU time of approximately 42.69 seconds, compared to 74.04 seconds for the original Merge Sort, representing approximately 42.3% lower CPU time in this experiment. These results show that the hybrid algorithm can achieve lower measured CPU time even when it performs more key comparisons. This indicates that key comparisons alone do not completely determine the actual execution time. The use of Insertion Sort for smaller subarrays can reduce some of the overhead associated with recursively splitting and merging small subarrays. However, these results are specific to the tested dataset, input size, threshold values, and experimental environment. Therefore, the results demonstrate the performance observed in this experiment rather than establishing that the hybrid algorithm will always outperform the original Merge Sort.