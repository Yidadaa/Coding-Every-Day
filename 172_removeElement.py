class Solution:
    """
    @param A: A list of integers
    @param elem: An integer
    @return: The new length after remove
    """
    def removeElement(self, A, elem):
        res = []
        length = 0
        max = len(A)
        i = 0
        while i < max:
            if A[i] == elem:
                del A[i]
                i = 0
                max = len(A)
            else:
                length += 1
                i += 1
        return length

print(Solution().removeElement([0,0,2,0,0,3,4,5,6], 0))