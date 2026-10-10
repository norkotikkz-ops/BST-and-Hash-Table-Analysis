"""Binary Search Tree (iterative, so sorted input with 10,000 keys does not hit recursion limit)."""


class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            self.size += 1
            return True
        cur = self.root
        while True:
            if key == cur.key:
                return False
            if key < cur.key:
                if cur.left is None:
                    cur.left = Node(key)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(key)
                    break
                cur = cur.right
        self.size += 1
        return True

    def search(self, key):
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def delete(self, key):
        parent, cur = None, self.root
        while cur is not None and cur.key != key:
            parent = cur
            cur = cur.left if key < cur.key else cur.right
        if cur is None:
            return False

        if cur.left is not None and cur.right is not None:
            succ_parent, succ = cur, cur.right
            while succ.left is not None:
                succ_parent, succ = succ, succ.left
            cur.key = succ.key
            parent, cur = succ_parent, succ

        child = cur.left if cur.left is not None else cur.right
        if parent is None:
            self.root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child
        self.size -= 1
        return True

    def height(self):
        if self.root is None:
            return 0
        h, level = 0, [self.root]
        while level:
            h += 1
            level = [c for n in level for c in (n.left, n.right) if c]
        return h

    def __len__(self):
        return self.size
