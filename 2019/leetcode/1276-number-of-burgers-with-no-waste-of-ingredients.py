class Solution:
    def numOfBurgers(self, tomatoSlices: int, cheeseSlices: int) -> List[int]:
        if tomatoSlices & 1 == 1 or tomatoSlices > 4 * cheeseSlices or tomatoSlices < 2 * cheeseSlices:
            return []
        return [(tomatoSlices >> 1) - cheeseSlices, 2 * cheeseSlices - (tomatoSlices >> 1)]
