class Solution:
    # @param strs: A list of strings
    # @return: A list of strings
    def anagrams(self, strs):
        hashTable = {}
        res = []
        for string in strs:
            sortedStr = "".join(sorted(string))
            if sortedStr in hashTable:
                hashTable[sortedStr].append(string)
            else:
                hashTable[sortedStr] = [string]
        for i in hashTable:
            i = hashTable[i]
            if len(i) > 1:
                res.extend(i)
        return res

print(Solution().anagrams(["nfsdf","afsdf","ssd","dss","as","sa"]))