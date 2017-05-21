class Solution:
    """
    @param A : a list of integers
    @param target : an integer to be inserted
    @return : an integer
    """
    def searchInsert(self, A, target):
        i = 0
        j = len(A)
        if j == 0 or target <= A[0]:
            return 0
        lastM = 0
        while True:
            m = int((i + j) / 2)
            if m == lastM:
                return m + 1
            if A[m] < target:
                i = m
            elif A[m] > target:
                j = m
            else:
                return m
            lastM = m

print(Solution().searchInsert([1, 2, 3], 4))