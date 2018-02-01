class Solution:
    """
    @param: : a continuous stream of numbers
    @param: : a number
    @return: returns the first unique number
    """

    def firstUniqueNumber(self, nums, number):
        # Write your code her
        dict = {}
        arrs = []
        for i in nums:
            if i in dict:
                dict[i] += 1
            else:
                dict[i] = 1
            if i == number:
                for i in dict.items():
                    if i[1] == 1:
                        arrs.append(i[0])
                for i in nums:
                    if i in arrs:
                        return i
        return -1