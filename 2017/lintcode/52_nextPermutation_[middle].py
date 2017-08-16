class Solution:
    # @param num :  a list of integer
    # @return : a list of integer
    def nextPermutation(self, num):
        length = len(num)
        if length == 0:
            return []
        if length == 1:
            return num
        else:
            if num[-1] > num[-2]:
                [num[-1], num[-2]] = [num[-2], num[-1]]
                return num
            else:
                i = length - 1
                while i > 0 and num[i] <= num[i - 1]:
                    i -= 1
                i -= 1
                if i == -1:
                    num.sort()
                    return num
                else:
                    index = i
                    i = length - 1
                    while i > index and num[i] <= num[index]:
                        i -= 1
                    [num[index], num[i]] = [num[i], num[index]]
                    res = num[0:index + 1]
                    tmp = num[index + 1:]
                    tmp.sort()
                    res.extend(tmp)
                    return res
test = [[1,2,3,4,5], [5,4,3,2,1],[1,2,3,5,4],[],[1],[1,2,5,3,3]]
print(list(map(lambda x:Solution().nextPermutation(x), test)))