import random
import time


# --------------------------------------------------
# INSERTION SORT
# --------------------------------------------------

def insertion_sort(arr, low, high, counter):
    for i in range(low + 1, high + 1):

        key = arr[i]
        j = i - 1

        while j >= low:

            # Count key comparison
            counter[0] += 1

            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = key


# --------------------------------------------------
# MERGE
# --------------------------------------------------

def merge(arr, low, mid, high, counter):

    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = 0
    j = 0
    k = low

    while i < len(left) and j < len(right):

        # Count key comparison
        counter[0] += 1

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


# --------------------------------------------------
# HYBRID SORT
# --------------------------------------------------

def hybrid(arr, low, high, s, counter):

    size = high - low + 1

    # Switch to insertion sort
    if size <= s:
        insertion_sort(arr, low, high, counter)
        return

    mid = (low + high) // 2

    hybrid(arr, low, mid, s, counter)
    hybrid(arr, mid + 1, high, s, counter)

    merge(arr, low, mid, high, counter)


# --------------------------------------------------
# HYBRID SORT WRAPPER
# --------------------------------------------------

def hybrid_sort(arr, s):

    counter = [0]

    if len(arr) <= 1:
        return arr, 0

    hybrid(arr, 0, len(arr) - 1, s, counter)

    return arr, counter[0]


# --------------------------------------------------
# DATASET GENERATION
# --------------------------------------------------

def generate_dataset(size, seed=42):

    rng = random.Random(seed)

    return [
        rng.randint(1, 10_000_000)
        for _ in range(size)
    ]


# --------------------------------------------------
# C-III EXPERIMENT
# --------------------------------------------------

S_VALUES = [
    1,
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    50
]


INPUT_SIZES = [
    10_000,
    100_000,
    1_000_000,
    5_000_000,
    10_000_000
]


for n in INPUT_SIZES:

    print("\n" + "=" * 70)
    print(f"INPUT SIZE n = {n:,}")
    print("=" * 70)

    # Generate ONE dataset for this n
    # Every S will use the SAME dataset
    original_data = generate_dataset(n, seed=42)

    for s in S_VALUES:

        # Make a copy so every S receives
        # exactly the same input
        data = original_data.copy()

        start_time = time.perf_counter()

        sorted_data, comparisons = hybrid_sort(data, s)

        end_time = time.perf_counter()

        cpu_time = end_time - start_time

        print(
            f"S = {s:2d} | "
            f"Comparisons = {comparisons:,} | "
            f"CPU Time = {cpu_time:.4f} seconds"
        )

        # Check correctness
        if sorted_data != sorted(original_data):
            print("ERROR: Sorting is incorrect!")
            break
