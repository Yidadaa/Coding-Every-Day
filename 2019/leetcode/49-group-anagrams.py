class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = dict()
        for s in strs:
            k = ''.join(sorted(list(s)))
            if k in d:
                d[k].append(s)
            else:
                d[k] = [s]
        return list(d.values())
