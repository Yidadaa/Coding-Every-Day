class Solution:
    import math
    def numberOfBoomerangs(self, points: List[List[int]]) -> int:
        d = {}
        N = len(points)
        i = 0
        while i < N:
            j = i + 1
            while j < N:
                dist = self.dist(points[i], points[j])
                if dist in d:
                    for x in [i, j]:
                        if x in d[dist]:
                            d[dist][x] += 1
                        else:
                            d[dist][x] = 1
                else:
                    d[dist] = { i: 1, j: 1 }
                j += 1
            i += 1

        ret = 0
        for dist in d:
            for p in d[dist]:
                pn = d[dist][p]
                ret += pn * (pn - 1) if pn > 1 else 0

        return ret

    def dist(self, p1, p2):
        a = p1[0] - p2[0]
        b = p1[1] - p2[1]
        return a*a + b*b
