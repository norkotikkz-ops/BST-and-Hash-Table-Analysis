"""Correctness tests: python test_structures.py"""
import random
from bst import BST
from hash_table import HashTable


def check(factory):
    ds = factory()
    keys = random.sample(range(5000), 1000)
    for k in keys:
        assert ds.insert(k)
    assert not ds.insert(keys[0])
    assert len(ds) == 1000
    assert all(ds.search(k) for k in keys)
    assert not ds.search(-1)
    random.shuffle(keys)
    for k in keys[:500]:
        assert ds.delete(k)
    assert not ds.delete(-1)
    assert all(not ds.search(k) for k in keys[:500])
    assert all(ds.search(k) for k in keys[500:])
    assert len(ds) == 500


if __name__ == "__main__":
    check(BST)
    check(HashTable)
    print("All tests passed")
