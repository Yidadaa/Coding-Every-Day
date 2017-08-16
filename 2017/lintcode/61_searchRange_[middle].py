class Solution:
    """
    @param A : a list of integers
    @param target : an integer to be searched
    @return : a list of length 2, [index1, index2]
    """
    def searchRange(self, A, target):
        i = 0
        j = len(A)
        lastM = -1
        if j == 0:
            return [-1, -1]
        while True:
            m = int((i + j) / 2)
            if m == lastM:
                return [-1, -1]
            if A[m] == target:
                index1 = m
                index2 = m
                while index1 > 0 and A[index1 - 1] == A[index1]:
                    index1 -= 1
                while index2 < len(A) - 1 and A[index2 + 1] == A[index2]:
                    index2 += 1
                return [index1, index2]
            elif A[m] > target:
                j = m
            elif A[m] < target:
                i = m
            lastM = m

test = [[5]]
print(list(map(lambda x: Solution().searchRange(x, 3), test)))