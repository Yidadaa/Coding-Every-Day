    class Solution:
        """
        @param: : sorted integer array A
        @param: : sorted integer array B
        @return: A new sorted integer array
        """

        def mergeSortedArray(self, A, B):
            res = []
            i = 0
            k = 0
            while True:
                if i < len(A) and k < len(B):
                    numA = A[i]
                    numB = B[k]
                    if numA < numB:
                        res.append(numA)
                        i += 1
                    else:
                        res.append(numB)
                        k += 1
                elif i == len(A) and k < len(B):
                    res.append(B[k])
                    k += 1
                elif i < len(A) and k == len(B):
                    res.append(A[i])
                    i += 1
                else:
                    break
            return res

print(Solution().mergeSortedArray([], []))