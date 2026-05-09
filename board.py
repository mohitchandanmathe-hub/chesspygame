from game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Black pieces (top)
        self.grid[0] = [
            Rook("black"), Knight("black"), Bishop("black"), Queen("black"),
            King("black"), Bishop("black"), Knight("black"), Rook("black")
        ]
        self.grid[1] = [Pawn("black") for _ in range(8)]

        # White pieces (bottom)
        self.grid[6] = [Pawn("white") for _ in range(8)]
        self.grid[7] = [
            Rook("white"), Knight("white"), Bishop("white"), Queen("white"),
            King("white"), Bishop("white"), Knight("white"), Rook("white")
        ]

    def get(self, row: int, col: int):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return self.grid[row][col]
        return None

    def set(self, row: int, col: int, piece):
        self.grid[row][col] = piece

    def move(self, from_row: int, from_col: int, to_row: int, to_col: int):
        piece = self.grid[from_row][from_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        if piece:
            piece.has_moved = True

    def find_king(self, color: str):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.symbol == "K" and piece.color == color:
                    return (row, col)
        return None

    def copy(self):
        import copy
        new_board = Board.__new__(Board)
        new_board.grid = copy.deepcopy(self.grid)
        return new_board