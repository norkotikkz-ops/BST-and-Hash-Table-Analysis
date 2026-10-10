# BST vs Hash Table — Performance Analysis

Bonus Task (REGMID +5%). Implementation and comparison of a **Binary Search Tree (BST)** and a **Hash Table** in Python 3.

## Files

| File | Description |
|---|---|
| `bst.py` | BST (iterative insert / search / delete, no recursion) |
| `hash_table.py` | Hash table with separate chaining + automatic resizing (load factor ≤ 0.75) |
| `benchmark.py` | Timing experiment for n = 100, 1,000, 10,000 |
| `test_structures.py` | Correctness tests |
| `results.csv` | Raw benchmark output |

## How to run

```bash
python test_structures.py   # correctness tests
python benchmark.py         # prints results and writes results.csv
```

No external libraries are needed.

## 1. Implementation

**BST** – every node has `key`, `left`, `right`. Smaller keys go left, larger keys go right. Delete handles three cases: leaf, one child, two children (replace with the in-order successor). Methods are iterative so a degenerate tree with 10,000 nodes does not exceed Python's recursion limit.

**Hash Table** – an array of buckets (lists). The index is `hash(key) % capacity`. Collisions are handled by **separate chaining**. When `size / capacity > 0.75`, the capacity doubles and all keys are re-hashed.

## 2. Complexity analysis

n = number of elements, h = height of the BST.

| Operation | BST best | BST average | BST worst | Hash best | Hash average | Hash worst |
|---|---|---|---|---|---|---|
| Insert | O(1) (root / short path) | O(log n) | **O(n)** | O(1) | O(1) amortized | **O(n)** |
| Search | O(1) (key at root) | O(log n) | **O(n)** | O(1) | O(1) | **O(n)** |
| Delete | O(1) (root leaf / short path) | O(log n) | **O(n)** | O(1) | O(1) | **O(n)** |

**Why:**

- **BST:** each operation walks one path from the root, so the cost is O(h). With random insertion order the tree is balanced on average, h ≈ log n. If keys are inserted in sorted order, the tree becomes a linked list (h = n) → O(n). This BST is *not* self-balancing (unlike AVL / Red-Black trees).
- **Hash Table:** the hash gives the bucket directly, then a short chain is scanned. With a good hash function and load factor ≤ 0.75, chains are short → O(1). Worst case is when all keys fall into one bucket (bad hash / many collisions) → one chain of length n → O(n). Insert is *amortized* O(1) because an occasional resize costs O(n).

## 3. Experiment

- Keys: unique random integers (`random.seed(42)`), inserted → all searched → all deleted.
- Each result is the **median of 5 runs** (the sorted-keys case for n = 10,000 is run once because it is slow).
- Times are the **total time for all n operations**, in milliseconds.
- Extra case: BST with **sorted keys** to demonstrate the worst case.

### Results (ms, total for n operations)

| Structure | n | Insert | Search | Delete |
|---|---|---|---|---|
| BST (random) | 100 | 0.031 | 0.022 | 0.025 |
| BST (sorted – worst case) | 100 | 0.128 | 0.111 | 0.009* |
| Hash Table | 100 | 0.056 | 0.009 | 0.012 |
| BST (random) | 1,000 | 0.481 | 0.344 | 0.420 |
| BST (sorted – worst case) | 1,000 | 12.001 | 10.889 | 0.093* |
| Hash Table | 1,000 | 0.500 | 0.087 | 0.124 |
| BST (random) | 10,000 | 6.686 | 4.956 | 5.586 |
| BST (sorted – worst case) | 10,000 | 1217.999 | 1170.114 | 0.986* |
| Hash Table | 10,000 | 5.650 | 0.983 | 1.288 |

\* Delete on the sorted tree is fast only because keys are deleted in sorted order: each deleted key is the current root, which has no left child, so deletion is O(1). Deleting in random order from the degenerate tree would be O(n) per operation.

BST heights for random keys: n = 100 → 14, n = 1,000 → 20, n = 10,000 → 30 (close to log₂ n, a bit larger because the tree is not perfectly balanced). In the sorted case the height equals n.

*(Exact times depend on the machine; run `benchmark.py` to reproduce. The trends are what matter.)*

### Comparison

- **Search:** the hash table is clearly faster — about 5× faster than the random BST at n = 10,000 (0.98 ms vs 4.96 ms). Its time grows roughly linearly with n (O(1) per operation), while the BST grows faster (O(log n) per operation).
- **Insert / Delete:** on random data both are in the same range; the hash table is slightly faster for delete. Insert is similar because the hash table pays for occasional resizing.
- **Worst case:** the BST on sorted input is extremely slow: n = 10,000 takes ~1.2 s for insert vs ~6.7 ms on random data (**~180× slower**). Growth from 1,000 → 10,000 is about 100×, which matches O(n²) total (O(n) per operation).

## 4. Why performance differs in practice

1. **Hashing jumps straight to the location**, while a BST needs several comparisons and pointer jumps (log n levels).
2. **Balance matters for BST.** Performance depends on the input order; sorted or nearly sorted data destroys the O(log n) guarantee. Self-balancing trees (AVL, Red-Black) fix this.
3. **Hash table performance depends on the hash function and load factor.** Poor hashing or a very high load factor creates long chains. Resizing keeps the load factor low but causes occasional expensive operations.
4. **Memory / cache:** BST nodes are separate objects scattered in memory (pointer chasing = cache misses); hash tables use a contiguous array of buckets, which is usually more cache-friendly.
5. **Ordering:** a BST keeps keys sorted, so it supports in-order traversal, min/max, range queries, predecessor/successor in O(h). A hash table cannot do these efficiently.
6. **Python overhead:** the numbers are from Python, where constant factors are large, so small n gives very small times that are affected by noise.

## 5. Conclusions

- For plain insert / search / delete by key, a **hash table is faster on average** (O(1) vs O(log n)), and the gap grows with n.
- A **plain BST can degrade to O(n)** on sorted input, as confirmed by the experiment; its guarantee depends on the tree staying balanced.
- Use a **hash table** when only fast lookup is needed; use a **BST (preferably balanced)** when sorted order or range queries are needed, or when predictable worst-case time is required (balanced trees guarantee O(log n)).
