class Solution:
    """
    @param numbersbers : Give an array numbersbers of n integer
    @return : Find all unique triplets in the array which gives the sum of zero.
    """
    def threeSum(self, numbers):
        '''
        这道题不会做，也是看了StackOverFlow上面大佬的代码才写出来的，
        主要是双指针的应用，排序之后用两根指针从头和尾遍历排序数组，可以
        节省很多的时间。核心思想是化无序为有序？而且中间很多省时间的步骤
        也值得学习，比如判断两个相邻的数是否相等，如果相等就略过。
        '''
        numbers.sort()
        res = []
        for i in range(len(numbers) - 2):
            if i == 0 or (i > 0 and numbers[i] != numbers[i - 1]):
                lo = i + 1
                hi = len(numbers) - 1
                sums = 0 - numbers[i]
                while lo < hi:
                    if numbers[lo] + numbers[hi] == sums:
                        res.append([numbers[i], numbers[lo], numbers[hi]])
                        while lo < hi and numbers[lo] == numbers[lo + 1]:
                            lo += 1
                        while lo < hi and numbers[hi] == numbers[hi - 1]:
                            hi -= 1
                        lo += 1
                        hi -= 1
                    elif numbers[lo] + numbers[hi] < sums:
                        while lo < hi and numbers[lo] == numbers[lo + 1]:
                            lo += 1
                        lo += 1
                    else:
                        while lo < hi and numbers[hi] == numbers[hi - 1]:
                            hi -= 1
                        hi -= 1
        return res

print(Solution().threeSum([1, 2, 3, 3, 7, -4, -6, -2, -1]))