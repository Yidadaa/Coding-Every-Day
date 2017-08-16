class Solution:
    """
    @param nums: The integer array you should partition
    @param k: As description
    @return: The index after partition
    """
    def partitionArray(self, nums, k):
        # write your code here
        # you should partition the nums by k
        # and return the partition index as description
        '''
        这是一道假的中等题，本质上其实是数组元素的移位，如果单纯的解题，
        只需要计算数组中比k小的数的数量就行了，即使题目中说明了不让这样做，
        也掩盖不了这道题出得失败的本质。
        '''
        length = len(nums)
        i = 0
        p = 0
        while i < length:
            if nums[i] < k:
                tmp = nums[i]
                del nums[i]
                nums.insert(0, tmp)
                p += 1
            i += 1
        return p

print(Solution().partitionArray([1, 2, 3, 4, 5], 8))