class Solution:
    """
    @param L: Given n pieces of wood with length L[i]
    @param k: An integer
    return: The maximum length of the small pieces.
    """
    def woodCut(self, L, k):
        if len(L) == 0 or max(L) == 0:
            return 0
        i = 0
        j = max(L)
        lastM = -1
        while True:
            m = int((i + j) / 2)
            if m == 0:
                return 0
            n = sum(map(lambda x: int(x / m), L))
            if m == lastM:
                if n < k:
                    return 0
                else:
                    return m
            if n >= k:
                i = m
            elif n < k:
                j = m
            # elif n == k:
                # return m
            lastM = m

test = [[12, 2, 4]]
print(list(map(lambda x: Solution().woodCut(x, 6), test)))