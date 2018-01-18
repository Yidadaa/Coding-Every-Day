"""
生成第k个排列

某个数列的第k个排列可以在小于o(logn)的时间复杂度下确定
因为全排列属于确定性推理，可以直接确定第n个状态
"""
import math
class Solution:
    """
    @param: n: n
    @param: k: the k th permutation
    @return: return the k-th permutation
    """
    def getPermutation(self, n, k):
        nums = list(range(1, n + 1))
        res = []
        if k > math.factorial(n) or k < 1:
            return ''.join(map(str, nums))
        k -= 1
        while k > 0:
            num = math.factorial(len(nums) - 1)
            i = k // num
            k = k % num
            res.append(nums[i])
            nums.remove(nums[i])
        if len(nums) == n:
            res = list(range(1, n + 1))
        else:
            res.extend(nums)
            
        return ''.join(map(str, res))

if __name__ == '__main__':
    testClass = Solution()
    testCase = 1
    res = testClass.getPermutation(testCase, 2)
    print(res)