class Solution:
    """
    @param nums: A list of integers
    @param k: As described
    @return: The majority number
    """
    def majorityNumber(self, nums, k):
        hashT = {}
        for i in nums:
            if i in hashT:
                hashT[i] += 1
                if hashT[i] >= float(len(nums)) / float(k):
                    return i
            else:
                hashT[i] = 1