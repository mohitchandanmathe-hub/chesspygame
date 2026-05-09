from game.board import Board
from game.rules import get_valid_moves, is_in_check, is_checkmate, is_stalemate


class GameState:
    PLAYING = "playing"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"


class Engine:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.selected = None        # (row, col) of selected piece
        self.valid_moves = []       # valid moves for selected piece
        self.state = GameState.PLAYING
        self.status_msg = "White's turn"
        self.move_history = []
        self.captured_white = []    # white pieces captured by black
        self.captured_black = []    # black pieces captured by white

    def select(self, row: int, col: int) -> bool:
        """Select a piece or move to target. Returns True if a move was made."""
        if self.state != GameState.PLAYING:
            return False

        piece = self.board.get(row, col)

        # If a piece is already selected
        if self.selected:
            # Try to move to clicked square
            if (row, col) in self.valid_moves:
                self._make_move(self.selected, (row, col))
                return True
            # Clicked own piece — reselect
            elif piece and piece.color == self.current_turn:
                self.selected = (row, col)
                self.valid_moves = get_valid_moves(
                    self.board, row, col
                )
                return False
            else:
                # Clicked empty or invalid — deselect
                self.selected = None
                self.valid_moves = []
                return False
        else:
            # Select a piece
            if piece and piece.color == self.current_turn:
                self.selected = (row, col)
                self.valid_moves = get_valid_moves(
                    self.board, row, col
                )
            return False

    def _make_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Track captured pieces
        target = self.board.get(to_row, to_col)
        if target:
            if target.color == "white":
                self.captured_white.append(target)
            else:
                self.captured_black.append(target)

        # Record move history
        piece = self.board.get(from_row, from_col)
        self.move_history.append(
            f"{self.current_turn[0].upper()}{piece.symbol} "
            f"({from_row},{from_col})→({to_row},{to_col})"
        )

        # Execute move
        self.board.move(from_row, from_col, to_row, to_col)

        # Pawn promotion
        moved = self.board.get(to_row, to_col)
        if moved and moved.symbol == "P":
            if (moved.color == "white" and to_row == 0) or \
               (moved.color == "black" and to_row == 7):
                from game.pieces import Queen
                self.board.set(to_row, to_col, Queen(moved.color))

        # Clear selection
        self.selected = None
        self.valid_moves = []

        # Switch turn
        self.current_turn = (
            "black" if self.current_turn == "white" else "white"
        )

        # Check game state
        self._update_state()

    def _update_state(self):
        color = self.current_turn

        if is_checkmate(self.board, color):
            winner = "Black" if color == "white" else "White"
            self.state = GameState.CHECKMATE
            self.status_msg = f"CHECKMATE! {winner} wins! 🎉"

        elif is_stalemate(self.board, color):
            self.state = GameState.STALEMATE
            self.status_msg = "STALEMATE! It's a draw!"

        elif is_in_check(self.board, color):
            self.status_msg = f"{color.capitalize()} is in CHECK!"

        else:
            self.status_msg = f"{self.current_turn.capitalize()}'s turn"

    def reset(self):
        self.__init__()