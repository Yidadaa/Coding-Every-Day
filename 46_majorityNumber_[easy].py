class Solution:
    """
    @param nums: A list of integers
    @return: The majority number
    """
    def majorityNumber(self, nums):
        # 额，好像到目前为止都没感受到贪心法的思想
        # 这些简单题的思路跟贪心有什么关系？
        # 这道题主要是利用主元素的性质，一一对应，多余的就是主元素
        if len(nums) == 0:
            return 0
        elif len(nums) == 1:
            return nums[0]
        count = 0
        majorNum = nums[0]
        length = len(nums)
        for i in range(length):
            if i == 0:
                continue
            if count == -1:
                count = 0
                majorNum = nums[i]
                continue
            if majorNum == nums[i]:
                count += 1
            else:
                count -= 1
            if count >= (length - i) / 2:
                break
        return majorNum

test = [[1, 2, 1, 2, 1], [1], [], [1, 1, 2, 1], [2, 3, 4, 1, 1, 1, 1], [1, 1]]
print(list(map(lambda x: Solution().majorityNumber(x), test)))