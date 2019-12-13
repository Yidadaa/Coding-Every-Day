class Solution:
    def minFlips(self, mat: List[List[int]]) -> int:
        self.n, self.m = len(mat), len(mat[0])
        states = [-1] * (1 << (self.n * self.m))
        init_state = self.mat2int(mat)
        # BFS search
        queue = [(init_state, 0)]
        while len(queue) > 0:
            next_state, step = queue.pop(-1)
            states[next_state] = step if states[next_state] == -1 else min(states[next_state], step)
            for new_state in self.get_adj_states(next_state):
                if states[new_state] == -1 or step + 1 < states[new_state]:
                    queue.append((new_state, step + 1))
        return states[0]
    
    def mat2int(self, mat):
        ret = 0
        for i in range(self.n * self.m):
            x, y = i // self.m, i % self.m
            ret += mat[x][y] << i
        return ret
    
    def get_adj_states(self, state):
        adj_states = []
        for x in range(self.n):
            for y in range(self.m):
                add_state = 0
                for (x_, y_) in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x, y)]:
                    if x_ >= 0 and x_ < self.n and y_ >= 0 and y_ < self.m:
                        pos = x_ * self.m + y_
                        add_state += (1 << pos)
                adj_states.append(state ^ add_state)
        return adj_states
