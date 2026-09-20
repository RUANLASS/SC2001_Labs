import random
import time
import csv

from hybrid_sort import hybrid_merge_insertion_sort

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

results = []

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

        start_time = time.process_time()

        _, comparisons = hybrid_merge_insertion_sort(data, s)

        end_time = time.process_time()

        cpu_time = end_time - start_time

        print(
            f"S = {s:2d} | "
            f"Comparisons = {comparisons:,} | "
            f"CPU Time = {cpu_time:.4f} seconds"
        )

        results.append([
            n, 
            s,
            comparisons,
            cpu_time
        ])

        
with open("c3_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Input Size",
        "S",
        "Key Comparisons",
        "CPU Time"
    ])

    writer.writerows(results)

print("\nResults saved to c3_results.csv")