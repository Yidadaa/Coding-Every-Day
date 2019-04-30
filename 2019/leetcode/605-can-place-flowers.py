class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        N = len(flowerbed)
        for i in range(N):
            if n <= 0:
                return True
            if (i == 0 or flowerbed[i - 1] == 0) and (i == N - 1 or flowerbed[i + 1] == 0) and flowerbed[i] == 0:
                n -= 1
                flowerbed[i] = 1
        return n <= 0
