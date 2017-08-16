class Solution:
    # @param n a integer
    # @return as a integer
    def trailingZeros(self, n):
        # 思路清奇
        if n <= 0:
            return 0
        else:
            count = 0
            while (int(n / 5)) != 0:
                count += int(n / 5)
                n = int(n / 5)
                
            return count