"""
经典二分查找
"""

class Solution:
    """
    @param: nums: An integer array sorted in ascending order
    @param: target: An integer
    @return: An integer
    """
    def findPosition(self, nums, target):
        midIndex = -1
        minIndex = 0
        maxIndex = len(nums) - 1
        lastIndex = maxIndex
        while maxIndex >= minIndex:
            lastIndex = midIndex
            midIndex = int((minIndex + maxIndex) / 2)
            if nums[midIndex] > target:
                maxIndex = midIndex
            elif nums[midIndex] < target:
                minIndex = midIndex
            else:
                break
            if lastIndex == midIndex:
                midIndex = midIndex + 1 if midIndex < len(nums) - 1 and nums[midIndex + 1] == target else -1
                break
        return midIndex

if __name__ == '__main__':
    testClass = Solution()
    testCase = [3]
    res = testClass.findPosition(testCase, 3)
    print(res)