class Node:
    def __init__(self, key, val, pre, next):
        self.key = key
        self.val = val
        self.pre = pre
        self.next = next


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        if node == self.head:
            return node.val
        if node == self.tail:
            self.tail = node.pre
        if node.pre:
            node.pre.next = node.next
        if node.next:
            node.next.pre = node.pre
        node.pre, node.next = None, self.head
        self.head.pre = node
        self.head = node
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.cache:
            self.cache[key].val = value
            self.get(key)
            return
        if len(self.cache) >= self.capacity:
            if self.tail:
                if self.tail.pre:
                    self.tail.pre.next = None
                tkey = self.tail.key
                self.tail = self.tail.pre
                del self.cache[tkey]
        node = Node(key, value, None, self.head)
        if self.head:
            self.head.pre = node
        self.cache[key] = node
        self.head = node
        if not self.tail:
            self.tail = node

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
