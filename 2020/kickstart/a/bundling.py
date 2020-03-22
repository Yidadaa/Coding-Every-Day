import heapq

def read_ints():
  return list(map(int, input().split(' ')))

class Node():
  def __init__(self, parent, val, children, count, l):
    self.parent = parent
    self.val = val
    self.children = children # type: dict
    self.count = count
    self.len = l
    self.edcount = 0

  def __str__(self):
    return '({}, {}, {}) -> '.format(self.val, self.len, self.count) + ', '.join([str(child) for child in self.children.values()])

  def __lt__(self, other):
    return self.count <= other.count

def solve():
  t = int(input())
  for case in range(1, t + 1):
    n, k = read_ints()
    prefix_tree = Node(None, '', {}, 0, 0)
    nodes = []
    for i in range(n):
      s = input()
      node = prefix_tree
      prefix_tree.count += 1
      for c in s:
        if c not in node.children:
          node.children[c] = Node(node, c, {}, 0, node.len + 1)
          nodes.append(node.children[c])
        node = node.children[c]
        node.count += 1
      node.edcount += 1
    ret = 0
    while max(nodes).count >= k:
      mnode = None
      for node in nodes:
        if node.count >= k:
          if not mnode or node < mnode: mnode = node
      if not mnode: break
      ret += mnode.len
      node = mnode
      while node:
        node.count -= k
        node.edcount -= k
        node = node.parent
      q = list(mnode.children.values())
      while q:
        node = q.pop()
        node.count -= k
        node.edcount -= k
        q += list(node.children.values())
    print('Case #{}: {}'.format(case, ret))

if __name__ == "__main__":
  solve()