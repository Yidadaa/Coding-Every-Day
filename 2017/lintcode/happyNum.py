class Solution:
    # @param {int} n an integer
    # @return {boolean} true if this is a happy number or false
    def isHappy(self, n):
        # Write your code here
        src = [n]
        tmp = None
        while n != 1:
            tmp = n
            n = sum(map(lambda x: int(x) * int(x), str(n)))
            if tmp == n or n in src:
                return False
            src.append(n)
        return True

print(Solution().isHappy(2))
