"""
Member C -- Part (d)
Compare original Merge Sort with Hybrid Merge+Insertion Sort
on 10 million integers.

Compares:
- Number of key comparisons
- CPU time

Hybrid uses the optimal S obtained from Part (c).
"""

import csv
import time

from hybrid_sort import hybrid_merge_insertion_sort
from generate_data import generate_dataset


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

N = 10_000_000
S_OPTIMAL = 10
SEED = 42


# --------------------------------------------------
# ORIGINAL MERGE SORT
# --------------------------------------------------

def merge(arr, low, mid, high):

    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = 0
    j = 0
    k = low

    comparisons = 0

    while i < len(left) and j < len(right):

        comparisons += 1

        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return comparisons


def merge_sort(arr, low, high):

    if low >= high:
        return 0

    mid = (low + high) // 2

    comparisons = merge_sort(arr, low, mid)

    comparisons += merge_sort(arr, mid + 1, high)

    comparisons += merge(arr, low, mid, high)

    return comparisons


def original_merge_sort(arr):

    if len(arr) <= 1:
        return arr, 0

    comparisons = merge_sort(
        arr,
        0,
        len(arr) - 1
    )

    return arr, comparisons


# --------------------------------------------------
# EXPERIMENT D
# --------------------------------------------------

print("=" * 70)
print("PART (D): ORIGINAL MERGE SORT VS HYBRID MERGE+INSERTION SORT")
print("=" * 70)

print(f"Input size: {N:,}")
print(f"Hybrid S: {S_OPTIMAL}")
print(f"Seed: {SEED}")
print()

# Generate ONE dataset.
# Both algorithms will receive exactly the same data.
original_data = generate_dataset(N, seed=SEED)


# --------------------------------------------------
# ORIGINAL MERGE SORT
# --------------------------------------------------

print("Running original Merge Sort...")

merge_data = original_data.copy()

start_time = time.process_time()

sorted_merge, merge_comparisons = original_merge_sort(merge_data)

end_time = time.process_time()

merge_cpu_time = end_time - start_time

print(
    f"Original Merge Sort | "
    f"Comparisons = {merge_comparisons:,} | "
    f"CPU Time = {merge_cpu_time:.6f} seconds"
)


# --------------------------------------------------
# HYBRID MERGE + INSERTION SORT
# --------------------------------------------------

print("Running Hybrid Merge+Insertion Sort...")

hybrid_data = original_data.copy()

start_time = time.process_time()

sorted_hybrid, hybrid_comparisons = hybrid_merge_insertion_sort(
    hybrid_data,
    S_OPTIMAL
)

end_time = time.process_time()

hybrid_cpu_time = end_time - start_time

print(
    f"Hybrid Sort (S={S_OPTIMAL}) | "
    f"Comparisons = {hybrid_comparisons:,} | "
    f"CPU Time = {hybrid_cpu_time:.6f} seconds"
)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

with open("d_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Algorithm",
        "Input Size",
        "S",
        "Key Comparisons",
        "CPU Time"
    ])

    writer.writerow([
        "Original Merge Sort",
        N,
        "N/A",
        merge_comparisons,
        merge_cpu_time
    ])

    writer.writerow([
        "Hybrid Merge+Insertion Sort",
        N,
        S_OPTIMAL,
        hybrid_comparisons,
        hybrid_cpu_time
    ])


print()
print("Results saved to d_results.csv")