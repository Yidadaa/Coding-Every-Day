class Solution:
    def findTheLongestSubstring(self, s: str) -> int:
        keys = ['a', 'e', 'i', 'o', 'u']
        count = { k: 0 for k in keys }

        state = {}
        for i in range(32):
            k = ''.join(str(i >> j & 1) for j in range(5))
            state[k] = -1

        ret = 0
        for i in range(len(s)):
            if s[i] in count: count[s[i]] += 1
            key = ''.join([str(count[k] % 2) for k in keys])
            if key == '00000': ret = max(ret, i + 1)
            elif state[key] < 0: state[key] = i
            else: ret = max(ret, i - state[key])
        return ret