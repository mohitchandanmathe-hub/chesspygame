import random
from game.rules import get_valid_moves


def get_ai_move(board, color: str, difficulty: str = "medium"):
    """Returns (from_row, from_col, to_row, to_col) for AI move."""
    all_moves = _get_all_moves(board, color)

    if not all_moves:
        return None

    if difficulty == "easy":
        return random.choice(all_moves)

    elif difficulty == "medium":
        # Prefer captures, then random
        captures = [m for m in all_moves if board.get(m[2], m[3]) is not None]
        if captures:
            return random.choice(captures)
        return random.choice(all_moves)

    elif difficulty == "hard":
        return _best_move(board, color, all_moves)

    return random.choice(all_moves)


def _get_all_moves(board, color):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece and piece.color == color:
                valid = get_valid_moves(board, row, col)
                for (tr, tc) in valid:
                    moves.append((row, col, tr, tc))
    return moves


def _piece_value(symbol: str) -> int:
    values = {
        "P": 10, "N": 30, "B": 30,
        "R": 50, "Q": 90, "K": 900
    }
    return values.get(symbol, 0)


def _score_board(board, color: str) -> int:
    opponent = "black" if color == "white" else "white"
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece:
                val = _piece_value(piece.symbol)
                if piece.color == color:
                    score += val
                else:
                    score -= val
    return score


def _best_move(board, color, all_moves):
    best = None
    best_score = float("-inf")

    for (fr, fc, tr, tc) in all_moves:
        test_board = board.copy()
        test_board.move(fr, fc, tr, tc)
        score = _score_board(test_board, color)
        # Add randomness to avoid repetition
        score += random.randint(0, 5)
        if score > best_score:
            best_score = score
            best = (fr, fc, tr, tc)

    return best