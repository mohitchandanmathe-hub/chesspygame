class Piece:
    def __init__(self, color: str, symbol: str):
        self.color = color  # 'white' or 'black'
        self.symbol = symbol
        self.has_moved = False

    def __repr__(self):
        return f"{self.color[0].upper()}{self.symbol}"


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "P")


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "R")


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "N")


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "B")


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "Q")


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "K")


# Unicode symbols for rendering
SYMBOLS = {
    "white": {
        "K": "♔", "Q": "♕", "R": "♖",
        "B": "♗", "N": "♘", "P": "♙"
    },
    "black": {
        "K": "♚", "Q": "♛", "R": "♜",
        "B": "♝", "N": "♞", "P": "♟"
    }
}


def get_symbol(piece: Piece) -> str:
    return SYMBOLS[piece.color][piece.symbol]
