class board:

    def __init__(self, board):
        self.board = board

    def setNumber(self, num, x, y):
        self.board[x][y] = num

    def possible(self, y, x, n):
        for i in range(9):
            if self.board[y][i] == n:
                return False
        for i in range(9):
            if self.board[i][x] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[y0 + i][x0 + j] == n:
                    return False
        return True

    def solve(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    for n in range(1, 10):
                        if board.possible(self, y, x, n):
                            self.board[y][x] = n
                            board.solve(self)
                            if 0 not in self.board:
                                break
                            self.board[y][x] = 0
                    return
        return self.board





