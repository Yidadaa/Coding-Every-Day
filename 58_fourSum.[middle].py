class Solution:
    """
    @param numbersbers : Give an array numbersbersbers of n integer
    @param target : you need to find four elements that's sum of target
    @return : Find all unique quadruplets in the array which gives the sum of 
              zero.
    """
    def fourSum(self ,numbers, target):
        length = len(numbers)
        if length < 4:
            return []
        numbers.sort()
        res = []
        loOut = 0
        while loOut < length - 4:
            hiOut = loOut + 1
            while hiOut < length - 3:
                loIn = hiOut + 1
                hiIn = length - 1
                while loIn < hiIn:
                    s = numbers[loOut] + numbers[loIn] + numbers[hiIn] + numbers[hiOut]
                    indexs = [loOut, loIn, hiIn, hiOut]
                    nums = [numbers[loOut], numbers[loIn], numbers[hiIn], numbers[hiOut]]
                    nums.sort()
                    if s == target and nums not in res:
                        res.append(nums)
                        loIn += 1
                        hiIn -= 1
                    elif s < target:
                        while numbers[loIn + 1] == numbers[loIn]:
                            loIn += 1
                        loIn += 1
                    else:
                        while numbers[hiIn - 1] == numbers[hiIn]:
                            hiIn -=1
                        hiIn -=1
                hiOut += 1
            loOut += 1
        return res

print(Solution().fourSum([-2,-3,5,-1,-4,5,-11,7,1,2,3,4,-7,-1,-2,-3,-4,-5], 2))