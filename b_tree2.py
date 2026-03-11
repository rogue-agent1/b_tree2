#!/usr/bin/env python3
"""B-Tree — balanced search tree for disk-based storage (order configurable)."""

class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []; self.values = []; self.children = []; self.leaf = leaf

class BTree:
    def __init__(self, order=4):
        self.order = order; self.root = BTreeNode(); self.t = order // 2
    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]: i += 1
        if i < len(node.keys) and key == node.keys[i]: return node.values[i]
        if node.leaf: return None
        return self.search(key, node.children[i])
    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self._split(new_root, 0); self.root = new_root
        self._insert_nonfull(self.root, key, value)
    def _insert_nonfull(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and key < node.keys[i]: i -= 1
            if i >= 0 and node.keys[i] == key: node.values[i] = value; return
            node.keys.insert(i + 1, key); node.values.insert(i + 1, value)
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            if len(node.children[i].keys) == self.order - 1:
                self._split(node, i)
                if key > node.keys[i]: i += 1
            self._insert_nonfull(node.children[i], key, value)
    def _split(self, parent, idx):
        child = parent.children[idx]; mid = len(child.keys) // 2
        new_node = BTreeNode(leaf=child.leaf)
        parent.keys.insert(idx, child.keys[mid])
        parent.values.insert(idx, child.values[mid])
        parent.children.insert(idx + 1, new_node)
        new_node.keys = child.keys[mid+1:]; new_node.values = child.values[mid+1:]
        child.keys = child.keys[:mid]; child.values = child.values[:mid]
        if not child.leaf:
            new_node.children = child.children[mid+1:]
            child.children = child.children[:mid+1]
    def inorder(self):
        result = []; self._inorder(self.root, result); return result
    def _inorder(self, node, result):
        for i in range(len(node.keys)):
            if not node.leaf: self._inorder(node.children[i], result)
            result.append((node.keys[i], node.values[i]))
        if not node.leaf and node.children: self._inorder(node.children[-1], result)

if __name__ == "__main__":
    bt = BTree(order=4)
    for i in [10, 20, 5, 6, 12, 30, 7, 17]: bt.insert(i, f"v{i}")
    print(f"Search 12: {bt.search(12)}")
    print(f"Search 99: {bt.search(99)}")
    print(f"Inorder: {bt.inorder()}")
