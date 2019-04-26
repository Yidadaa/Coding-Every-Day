class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        if len(points) == 0:
            return 0

        d = {}
        maxd = 1
        for i in range(0, len(points)):
            for j in range(i + 1, len(points)):
                k = self.getKey(points[i], points[j])
                if k in d:
                    d[k].add(i)
                    d[k].add(j)
                    dkn = len(d[k])
                    maxd = max(maxd, dkn)
                else:
                    d[k] = set([i, j])
                    maxd = max(maxd, 2)
        print(d)
        return maxd
    
    def gcd(self, a, b):
        x = max(a, b)
        y = min(a, b)
        d = 1
        while y != 0:
            c = x % y
            if c == 0:
                d = y
                break
            x = y
            y = c
        x = a // d
        y = b // d
        return str(x) + '/' + str(y)
    
    def getKey(self, a, b):
        if a[0] == b[0]:
            if a[1] == b[1]:
                return '*' + str(a[0])
            return '_' + str(a[0])
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        k = self.gcd(dx, dy) if dy != 0 else 0
        db = dx*a[1] - dy*a[0]
        b = self.gcd(db, dx) if db != 0 else 0
        return (str(k)) + '_' + str(b)
