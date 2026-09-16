import random

DEFAULT_X = 10_000_000

DEFAULT_SIZES = [
    1_000,
    10_000,
    100_000,
    1_000_000,
    2_000_000,
    3_000_000,
    4_000_000,
    5_000_000,
    6_000_000,
    7_000_000,
    8_000_000,
    9_000_000,
    10_000_000,
]

#size -> size of array you want to generate, x -> max range you want to choose each element from
def generate_dataset(size, x=DEFAULT_X, seed=None):
    rng = random.Random(seed)
    return [rng.randint(1, x) for _ in range(size)]

#sizes -> list of all sizes you want to use
def generate_all(x= DEFAULT_X, sizes=DEFAULT_SIZES, seed_base=42):
    datasets = {}
    for i, size in enumerate(sizes):
        data = generate_dataset(size, x=x, seed=seed_base + i)
        datasets[size] = data
        print(f"Generated size={size:>10,}")

    return datasets


if __name__ == "__main__":
    generate_all()