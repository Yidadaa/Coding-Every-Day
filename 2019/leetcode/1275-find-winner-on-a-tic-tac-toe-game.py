class Solution:
    def tictactoe(self, moves: List[List[int]]) -> str:
        chessboard = [0] * 9
        for i, m in enumerate(moves): chessboard[m[0] * 3 + m[1]] = (i & 1) + 1
            
        for c in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
            if chessboard[c[0]] == chessboard[c[1]] == chessboard[c[2]] and chessboard[c[0]] > 0:
                return 'A' if chessboard[c[0]] == 1 else 'B'
            
        return 'Draw' if len(moves) == 9 else 'Pending'
