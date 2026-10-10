"""Benchmark BST vs Hash Table for n = 100, 1000, 10000."""
import csv
import random
import time

from bst import BST
from hash_table import HashTable

SIZES = [100, 1000, 10000]
REPEATS = 5


def timed(fn):
    t = time.perf_counter()
    fn()
    return time.perf_counter() - t


def run(structure_factory, keys):
    ds = structure_factory()
    t_ins = timed(lambda: [ds.insert(k) for k in keys])
    t_srch = timed(lambda: [ds.search(k) for k in keys])
    t_del = timed(lambda: [ds.delete(k) for k in keys])
    assert len(ds) == 0
    return t_ins, t_srch, t_del


def median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2]


def main():
    random.seed(42)
    rows = []
    for n in SIZES:
        random_keys = random.sample(range(10 * n), n)
        sorted_keys = sorted(random_keys)
        cases = [
            ("BST (random keys)", BST, random_keys),
            ("BST (sorted keys - worst case)", BST, sorted_keys),
            ("Hash Table (random keys)", HashTable, random_keys),
        ]
        for name, factory, keys in cases:
            reps = 1 if "sorted" in name and n >= 10000 else REPEATS
            res = [run(factory, keys) for _ in range(reps)]
            ins, srch, dele = (median([r[i] for r in res]) for i in range(3))
            rows.append([name, n, ins * 1000, srch * 1000, dele * 1000])
            print(f"n={n:>6} {name:<32} insert={ins*1000:10.3f} ms  "
                  f"search={srch*1000:10.3f} ms  delete={dele*1000:10.3f} ms")

    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["structure", "n", "insert_ms", "search_ms", "delete_ms"])
        for r in rows:
            w.writerow([r[0], r[1]] + [f"{x:.3f}" for x in r[2:]])

    random.seed(42)
    for n in SIZES:
        t = BST()
        for k in random.sample(range(10 * n), n):
            t.insert(k)
        print(f"BST height (random, n={n}): {t.height()}")


if __name__ == "__main__":
    main()
