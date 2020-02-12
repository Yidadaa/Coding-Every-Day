class Solution:
    def findDisappearedNumbers(self, nums):
        nums = [x - 1 for x in nums]
        i = 0
        while i < len(nums):
            if nums[i] == i or nums[nums[i]] == nums[i]: i += 1
            else:
                tmp, nums[i] = nums[i], nums[nums[i]]
                nums[tmp] = tmp
        ret = []
        for i in range(len(nums)):
            if i != nums[i]: ret.append(i + 1)
        return ret

if __name__ == "__main__":
    Solution().findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1])