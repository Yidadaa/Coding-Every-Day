class Solution:
    def findSmallestRegion(self, regions: List[List[str]], region1: str, region2: str) -> str:
        tree = {}
        head = set()
        parents = {}
        
        for region in regions:
            k, v = region[0], region[1:]
            if k not in tree: tree[k] = set()
            tree[k] |= set(v)
            
            head.add(k)
            head -= tree[k]
            
        tree['root'] = head
            
        stack = ['root']
        while len(stack) > 0:
            node = stack.pop()
            if node not in tree: continue
            for child in tree[node]:
                parents[child] = node
                stack.append(child)
                
        def find(x):
            path = [x]
            while path[-1] != 'root':
                path.append(parents[path[-1]])
            return path
                
        path1 = find(region1)
        path2 = find(region2)
        
        ret = ''
        p1, p2 = len(path1) - 1, len(path2) - 1
        while path1[p1] == path2[p2]:
            ret = path1[p1]
            p1 -= 1
            p2 -= 1
            
        return ret
