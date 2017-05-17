class Solution:
    """
    @param numbers : An array of Integer
    @param target : target = numbers[index1] + numbers[index2]
    @return : [index1 + 1, index2 + 1] (index1 < index2)
    """
    def twoSum(self, numbers, target):
        arr = map(lambda x: target - x, numbers)
        for i in range(len(numbers)):
            if numbers[i] in arr:
                for k in range(len(numbers)):
                    if i != k and arr[k] == numbers[i]:
                        return [i + 1, k + 1]
        return [0, 0]