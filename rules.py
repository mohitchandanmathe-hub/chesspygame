from game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


def get_valid_moves(board, row: int, col: int) -> list:
    piece = board.get(row, col)
    if not piece:
        return []

    raw_moves = _get_raw_moves(board, row, col)

    # Filter moves that would leave own king in check
    valid = []
    for (tr, tc) in raw_moves:
        test_board = board.copy()
        test_board.move(row, col, tr, tc)
        if not is_in_check(test_board, piece.color):
            valid.append((tr, tc))

    return valid


def _get_raw_moves(board, row, col) -> list:
    piece = board.get(row, col)
    if isinstance(piece, Pawn):
        return _pawn_moves(board, row, col, piece.color)
    elif isinstance(piece, Rook):
        return _sliding_moves(board, row, col, piece.color,
                              [(1,0),(-1,0),(0,1),(0,-1)])
    elif isinstance(piece, Bishop):
        return _sliding_moves(board, row, col, piece.color,
                              [(1,1),(1,-1),(-1,1),(-1,-1)])
    elif isinstance(piece, Queen):
        return _sliding_moves(board, row, col, piece.color,
                              [(1,0),(-1,0),(0,1),(0,-1),
                               (1,1),(1,-1),(-1,1),(-1,-1)])
    elif isinstance(piece, Knight):
        return _knight_moves(board, row, col, piece.color)
    elif isinstance(piece, King):
        return _king_moves(board, row, col, piece.color)
    return []


def _pawn_moves(board, row, col, color) -> list:
    moves = []
    direction = -1 if color == "white" else 1
    start_row = 6 if color == "white" else 1

    # Move forward
    nr = row + direction
    if 0 <= nr <= 7 and board.get(nr, col) is None:
        moves.append((nr, col))
        # Double move from start
        if row == start_row and board.get(nr + direction, col) is None:
            moves.append((nr + direction, col))

    # Captures
    for dc in [-1, 1]:
        nc = col + dc
        if 0 <= nc <= 7 and 0 <= nr <= 7:
            target = board.get(nr, nc)
            if target and target.color != color:
                moves.append((nr, nc))

    return moves


def _sliding_moves(board, row, col, color, directions) -> list:
    moves = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        while 0 <= nr <= 7 and 0 <= nc <= 7:
            target = board.get(nr, nc)
            if target is None:
                moves.append((nr, nc))
            elif target.color != color:
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def _knight_moves(board, row, col, color) -> list:
    moves = []
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),
                   (1,-2),(1,2),(2,-1),(2,1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr <= 7 and 0 <= nc <= 7:
            target = board.get(nr, nc)
            if target is None or target.color != color:
                moves.append((nr, nc))
    return moves


def _king_moves(board, row, col, color) -> list:
    moves = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                target = board.get(nr, nc)
                if target is None or target.color != color:
                    moves.append((nr, nc))
    return moves


def is_in_check(board, color: str) -> bool:
    king_pos = board.find_king(color)
    if not king_pos:
        return False
    opponent = "black" if color == "white" else "white"
    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece and piece.color == opponent:
                if king_pos in _get_raw_moves(board, row, col):
                    return True
    return False


def is_checkmate(board, color: str) -> bool:
    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece and piece.color == color:
                if get_valid_moves(board, row, col):
                    return False
    return is_in_check(board, color)


def is_stalemate(board, color: str) -> bool:
    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)
            if piece and piece.color == color:
                if get_valid_moves(board, row, col):
                    return False
    return not is_in_check(board, color)