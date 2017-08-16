class Solution:
    """
    @param A: a list of integers
    @return an integer
    """
    def removeDuplicates(self, A):
        times = 0
        length = len(A)
        if length == 0:
            return 0
        i = 0
        while i < length:
            if i == 0:
                times = 1
            else:
                if A[i] == A[i - 1]:
                    if times == 2:
                        del A[i]
                        length -= 1
                        continue
                    else:
                        times += 1
                else:
                    times = 1
            i += 1
        return len(A)

print(Solution().removeDuplicates([]))