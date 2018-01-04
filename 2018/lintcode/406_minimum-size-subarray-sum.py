class Solution:
    """
    @param: nums: an array of integers
    @param: s: An integer
    @return: an integer representing the minimum size of subarray
    """
    def minimumSize(self, nums, s):
        """
        子数组原来是数组的一部分，而不是数组中的元素组成的数组
        一般用两指针法遍历子数组
        """
        if sum(nums) < s:
            return -1
        res = float('inf')
        ss = 0
        sp = 0
        ep = 0
        while ep < len(nums):
            while ss < s and ep < len(nums):
                ss += nums[ep]
                ep += 1
            res = min(ep - sp, res)
            while ss >= s and sp < ep:
                ss -= nums[sp]
                sp += 1
            res = min(ep - sp + 1, res)
        return -1 if res == float('inf') else res

def test():
    """
    Test code here.
    """
    testInstance = Solution()
    testValue = [100, 50, 99, 50, 100, 50, 99, 50, 100, 50]
    s = 0
    print(testInstance.minimumSize(testValue, s))

if __name__ == '__main__':
    test()