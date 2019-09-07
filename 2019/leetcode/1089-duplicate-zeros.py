class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        Do not return anything, modify arr in-place instead.
        """
        c, l, n = -1, 0, len(arr)
        while c < n and l < n:
            c += 1 if arr[l] > 0 else 2
            l += 1
        while l > 0:
            step = 1 if arr[l - 1] > 0 else 2
            for s in range(step):
                if c < n: arr[c] = arr[l - 1]
                c -= 1
            l -= 1
            
