class Solution:
    # @param nums: The integer array
    # @param target: Target number to find
    # @return the first position of target in nums, position start from 0 
    def binarySearch(self, nums, target):
        '''
        有两点需要注意：
        1. target不一定在数组中
        2. 返回值是target第一次出现在数组中的位置
        '''
        A = nums
        i = 0
        j = len(A)
        if j == 0 or target < A[0]:
            return -1
        lastM = 0
        while True:
            m = int((i + j) / 2)
            if m == lastM or A[m] == target:
                break
            if A[m] < target:
                i = m
            elif A[m] > target:
                j = m
            lastM = m
        if A[m] == target:
            while m > 0 and A[m] == A[m - 1]:
                m -=1
            return m
        else:
            return -1

test = [[[2,2,2,2,2,2,2,2,3,4],2,0], [[1,2,3], 3, 2], [[1,2],-1,-1], [[],1,-1], [[1],1,0], [[4,5,9,9,12,13,14,15,15,18], 10,-1]]
print(list(map(lambda x: Solution().binarySearch(x[0], x[1]) == x[-1], test)))
print(Solution().binarySearch([4,5,9,9,12,13,14,15,15,18], 10))