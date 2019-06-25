class NumArray:

    def __init__(self, nums: List[int]):
        self.sums = [0] * (len(nums))
        self.nums = nums
        s = 0
        for i in range(len(nums)):
            s += nums[i]
            self.sums[i] = s

    def sumRange(self, i: int, j: int) -> int:
        return self.sums[j] - self.sums[i] + self.nums[i]
