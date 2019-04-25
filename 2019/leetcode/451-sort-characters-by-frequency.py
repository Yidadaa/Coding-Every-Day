class Solution:
    def frequencySort(self, s: str) -> str:
        d = {}
        for c in s:
            if c in d:
                d[c] += 1
            else:
                d[c] = 1
        k = list(d.keys())
        k = sorted(k, key=lambda x: d[x], reverse=True)
        ret = ''
        for x in k:
            s = d[x]
            while s > 0:
                ret += x
                s -= 1
        return ret