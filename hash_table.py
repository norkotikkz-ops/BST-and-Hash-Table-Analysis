"""Hash Table with separate chaining and automatic resizing (load factor <= 0.75)."""


class HashTable:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _index(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        for bucket in old:
            for key in bucket:
                self.buckets[self._index(key)].append(key)

    def insert(self, key):
        bucket = self.buckets[self._index(key)]
        if key in bucket:
            return False
        bucket.append(key)
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._resize()
        return True

    def search(self, key):
        return key in self.buckets[self._index(key)]

    def delete(self, key):
        bucket = self.buckets[self._index(key)]
        if key in bucket:
            bucket.remove(key)
            self.size -= 1
            return True
        return False

    def __len__(self):
        return self.size
