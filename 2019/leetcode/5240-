class Solution:
    def maxLength(self, arr: List[str]) -> int:
        stack = []
        
        for s in arr:
            if len(set(s)) == len(s): stack.append([s])
        
        while len(stack) > 1:
            new_stack = []
            while len(stack) > 0:
                next_node = []
                l = [] if len(stack) == 0 else stack.pop(0)
                r = [] if len(stack) == 0 else stack.pop(0)
                next_node += l + r
                for s in l:
                    table = {x: 0 for x in 'abcdefghijklmnopqrstuvwxyz'}
                    for c in s: table[c] = 1
                    for rs in r:
                        if all([table[c] == 0 for c in rs]):
                            next_node.append(s + rs)
                new_stack.append(next_node)
            stack = new_stack
        ret = 0
        if len(stack) > 0:
            for s in stack[0]:
                ret = max(ret, len(s))
        return ret
