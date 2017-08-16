class Solution:	
    #@param num: A list of non negative integers
    #@return: A string
    def largestNumber(self, num):
        # nlogn的复杂度，用快排
        # 重点是比较函数，有几种情况需要特殊考虑
        # 1. 常规情况，'12' < '2'
        # 2. 特殊情况，'20' < '203' && '20' > '201' && '20' < '202
        # 3. 边界条件，[] -> '' && [0, 0, 0] -> '0'
        if len(num) == 0:
            return ''
        if sum(num) == 0:
            return '0'
        self.quickSort(num)
        return ''.join(map(str, self.quickSort(num)))
    def quickSort(self, arr):
        length = len(arr)
        if length <= 1:
            return arr # 只剩一个值时直接返回
        flagIndex = int(length / 2)
        flag = arr[flagIndex]
        flagList = []
        lessList = []
        greaterList = []
        for i in arr:
            if self.compare(i, flag) == '>':
                greaterList.append(i)
            elif self.compare(i, flag) == '<':
                lessList.append(i)
            else:
                flagList.append(i)
        res = []
        res.extend(self.quickSort(greaterList))
        res.extend(flagList)
        res.extend(self.quickSort(lessList))
        return res

    def compare(self, a, b):
        # 比较两个数字的大小
        strA = str(a)
        strB = str(b)
        if strA[0] != strB[0]:
            numA = int(strA[0])
            numB = int(strB[0])
        else:
            length = min(len(strA), len(strB))
            for i in range(length):
                if int(strA[i]) == int(strB[i]):
                    numA = numB = -1
                    continue
                else:
                    numA = int(strA[i])
                    numB = int(strB[i])
                    break
        if numA == -1 and numB == -1 and len(strA) != len(strB):
            [minS, maxS] = [strA, strB] if len(strA) < len(strB) else [strB, strA]
            numA = int(minS + minS[0])
            numB = int(maxS[0:len(minS) + 1])
            numB = numB + 1 if numA == numB else numB
            [numA, numB] = [numA, numB] if len(strA) < len(strB) else [numB, numA]
        return '>' if  numA > numB else '<' if numA < numB else '='

test = [[5, 2, 1, 404, 40]]
print(list(map(lambda x: Solution().largestNumber(x), test)))