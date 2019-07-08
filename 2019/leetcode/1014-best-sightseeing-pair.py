class Solution:
    def maxScoreSightseeingPair(self, A: List[int]) -> int:
        max_i = -1
        ret = -1
        for i in range(len(A)):
            ret = max(ret, max_i + A[i] - i)
            max_i = max(max_i, A[i] + i)
        return ret
