class Solution:
    def countVowelPermutation(self, n: int) -> int:
        MOD = 1e9 + 7
        
        table = {
            'a': 1,
            'e': 1,
            'i': 1,
            'o': 1,
            'u': 1
        }
        
        state = {
            'a': ['e'],
            'e': ['a', 'i'],
            'i': ['a', 'e', 'o', 'u'],
            'o': ['i', 'u'],
            'u': ['a']
        }
        
        for i in range(n - 1):
            _table = {k:0 for k in table}
            for cur in state:
                for nex in state[cur]:
                    _table[nex] = (_table[nex] + table[cur]) % MOD
            table = _table
            
        return int(sum(table.values()) % MOD)
# 状态机，没什么好说的
