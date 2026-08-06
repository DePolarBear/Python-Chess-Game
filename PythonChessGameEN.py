import pygame

pygame.init()

# --- Constants (values that never change) ---
SQUARE = 100
BOARD = SQUARE * 8           # 800 - board size (width and height)
PANEL = 200                  # width of the side panel
WIDTH = BOARD + PANEL        # total window width
HEIGHT = BOARD               # window height = board height

# Square colors (RGB)
LIGHT = (240, 217, 181)      # light square
DARK  = (181, 136, 99)       # dark square

font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")
clock = pygame.time.Clock()

images = {}                           # empty dict, we fill it below
for letter in "PRNBQKprnbqk":         # go through all 12 letters
    if letter.isupper():
        color = "w"
    else:
        color = "b"
    name = "pieces/" + color + letter.upper() + ".svg"   # e.g. pieces/wP.svg
    img = pygame.image.load_sized_svg(name, (SQUARE, SQUARE))
    img = img.convert_alpha()
    images[letter] = img

def draw_board():
    for row in range(8):                # 0 to 7 (eight rows)
        for col in range(8):            # 0 to 7 (eight columns)
            # alternate colors: even sum -> light, otherwise dark
            if (row + col) % 2 == 0:
                color = LIGHT
            else:
                color = DARK
            # rectangle: (x, y, width, height)
            x = col * SQUARE
            y = row * SQUARE
            pygame.draw.rect(screen, color, (x, y, SQUARE, SQUARE))

def draw_pieces():
    for row in range(8):                # 0 to 7 (eight rows)
        for col in range(8):            # 0 to 7 (eight columns)
            piece = board[row][col]
            if piece != ".":            # only draw if there is a piece
                img = images[piece]
                x = col * SQUARE
                y = row * SQUARE
                screen.blit(img, (x, y))

def draw_selection():
    if selected is None:
        return
    row, col = selected
    x = col * SQUARE
    y = row * SQUARE
    pygame.draw.rect(screen, (0, 150, 0), (x, y, SQUARE, SQUARE), 2)

def draw_moves():
    if selected is None:
        return
    sel_row, sel_col = selected
    piece = board[sel_row][sel_col]
    highlight = pygame.Surface((SQUARE, SQUARE))   # small surface the size of a square
    highlight.set_alpha(50)                        # transparency: 0 = invisible, 255 = solid
    highlight.fill((0, 200, 0))                    # fill with green

    for r in range(8):
        for c in range(8):
            if is_move_valid(board, piece, sel_row, sel_col, r, c):
                x = c * SQUARE
                y = r * SQUARE
                screen.blit(highlight, (x, y))


def is_path_clear(board, old_row, old_col, new_row, new_col):
    d_row = new_row - old_row
    d_col = new_col - old_col

    if d_row > 0:
        step_row = 1
    elif d_row < 0:
        step_row = -1
    else:
        step_row = 0

    if d_col > 0:
        step_col = 1
    elif d_col < 0:
        step_col = -1
    else:
        step_col = 0

    r = old_row + step_row
    c = old_col + step_col
    # walk until we reach the target
    while (r, c) != (new_row, new_col):
        if board[r][c] != ".":
            return False        # something is in the way
        r = r + step_row        # next step
        c = c + step_col
    return True

def is_move_valid(board, piece, old_row, old_col, new_row, new_col):
    target = board[new_row][new_col]
    if (new_row, new_col) == (old_row, old_col):
        return False
    if target != "." and target.isupper() == piece.isupper():
        return False
    else:
        d_row = new_row - old_row
        d_col = new_col - old_col

        if piece.lower() == "r":
            if (d_row == 0 or d_col == 0) and is_path_clear(board, old_row, old_col, new_row, new_col):
                return True
            else:
                return False
        if piece.lower() == "b":
            if (abs(d_row) == abs(d_col)) and is_path_clear(board, old_row, old_col, new_row, new_col):
                return True
            else:
                return False
        if piece.lower() == "q":
            if (d_row == 0 or d_col == 0 or abs(d_row) == abs(d_col)) and is_path_clear(board, old_row, old_col, new_row, new_col):
                return True
            else:
                return False
        if piece.lower() == "n":
            if (abs(d_row) == 2 and abs(d_col) == 1) or (abs(d_row) == 1 and abs(d_col) == 2):
                return True
            else:
                return False
        if piece.lower() == "k":
            if abs(d_row) <= 1 and abs(d_col) <= 1:
                return True
            else:
                return False
        if piece.lower() == "p":
            if piece.isupper():
                direction = -1       # white moves up (smaller rows)
                start = 6
            else:
                direction = 1        # black moves down (larger rows)
                start = 1
            if d_col == 0 and d_row == direction and target == ".":
                return True
            if (d_col == 0 and d_row == 2 * direction and target == "." and old_row == start) and is_path_clear(board, old_row, old_col, new_row, new_col):
                return True
            if abs(d_col) == 1 and d_row == direction and target != ".":
                return True

        return False

def is_check(board, color):
    if color == "w":
        king = "K"
    else:
        king = "k"

    if color == "w":
        enemy_color = "b"
    else:
        enemy_color = "w"

    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                king_row = r
                king_col = c
    for r in range(8):
        for c in range(8):
            f = board[r][c]
            if f != ".":
                if f.isupper():
                    f_color = "w"
                else:
                    f_color = "b"
                if f_color == enemy_color:
                    if is_move_valid(board, f, r, c, king_row, king_col):
                        return True
    return False

def leaves_king_in_check(board, color, old_row, old_col, new_row, new_col):
    piece = board[old_row][old_col]          # the piece we are moving
    original_target = board[new_row][new_col]  # what was on the target (enemy or dot)
    board[new_row][new_col] = piece
    board[old_row][old_col] = "."
    in_check = is_check(board, color)
    board[old_row][old_col] = piece
    board[new_row][new_col] = original_target
    return in_check

def has_legal_move(board, color):
    for fr in range(8):                 # piece: row
        for fc in range(8):             # piece: column
            f = board[fr][fc]
            if f == ".":
                continue
            if f.isupper():
                f_color = "w"
            else:
                f_color = "b"
            if f_color != color:
                continue

            for tr in range(8):         # target: row
                for tc in range(8):     # target: column
                    if is_move_valid(board, f, fr, fc, tr, tc) and not leaves_king_in_check(board, color, fr, fc, tr, tc):
                        return True
    return False

def is_castling_possible(board, color, old_row, old_col, new_col, white_king_moved, black_king_moved, rook_moved):
    # king's row by color
    if color == "w":
        r = 7
        king_moved = white_king_moved
    else:
        r = 0
        king_moved = black_king_moved

    # 1) king must not have moved
    if king_moved:
        return False

    # 2) king must not be in check right now
    if is_check(board, color):
        return False

    if new_col == 6:
        # SHORT castling (kingside, rook in corner column 7)
        rook_col = 7
        between = [5, 6]         # these columns must be empty
        passing = [4, 5, 6]      # king passes through these (must not be attacked)
    elif new_col == 2:
        # LONG castling (queenside, rook in corner column 0)
        rook_col = 0
        between = [1, 2, 3]
        passing = [4, 3, 2]
    else:
        return False             # not a valid castling target

    if rook_moved[(r, rook_col)]:
        return False

    if color == "w":
        rook = "R"
    else:
        rook = "r"
    if board[r][rook_col] != rook:
        return False

    for c in between:
        if board[r][c] != ".":
            return False

    king_letter = board[r][old_col]          # king (K or k)
    for c in passing:
        original = board[r][c]
        board[r][old_col] = "."              # clear the original square
        board[r][c] = king_letter            # put the king on the tested square
        attacked = is_check(board, color)
        board[r][c] = original
        board[r][old_col] = king_letter
        if attacked:
            return False

    return True

def draw_end():
    if game_over is None:
        return
    bar = pygame.Surface((BOARD, 100))     # as wide as the board, 100 px tall
    bar.set_alpha(200)                      # fairly opaque so the text stands out
    bar.fill((0, 0, 0))                     # black background
    screen.blit(bar, (0, HEIGHT // 2 - 50)) # vertically centered (half height minus half bar)
    img = font.render(game_over, True, (255, 255, 255))
    w = img.get_width()
    h = img.get_height()
    x = BOARD // 2 - w // 2
    y = HEIGHT // 2 - h // 2
    screen.blit(img, (x, y))

    pygame.draw.rect(screen, (70, 70, 70), restart_btn)          # gray button rectangle
    text_btn = small_font.render("Restart", True, (255, 255, 255))
    # center the text on the button:
    tx = restart_btn.centerx - text_btn.get_width() // 2
    ty = restart_btn.centery - text_btn.get_height() // 2
    screen.blit(text_btn, (tx, ty))

def draw_check():
    for color in ("w", "b"):              # check both kings
        if is_check(board, color):         # is this king in check?
            if color == "w":
                king = "K"
            else:
                king = "k"
            # find the king on the board and highlight its square
            for r in range(8):
                for c in range(8):
                    if board[r][c] == king:
                        x = c * SQUARE
                        y = r * SQUARE
                        pygame.draw.rect(screen, (200, 0, 0), (x, y, SQUARE, SQUARE), 2)

def draw_turn():
    if turn == "w":
        # white is at the bottom - bar at the bottom
        pygame.draw.rect(screen, (0, 200, 0), (0, HEIGHT - 4, BOARD, 4))
    else:
        # black is at the top - bar at the top
        pygame.draw.rect(screen, (0, 200, 0), (0, 0, BOARD, 4))

def new_board():
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p"] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["P"] * 8,
        ["R","N","B","Q","K","B","N","R"],
    ]

def draw_clock():
    # black - at the very top, centered
    cb = int(time_b)
    text_b = f"{cb // 60}:{cb % 60:02d}"
    img_b = font.render(text_b, True, (255, 255, 255))
    xb = BOARD + PANEL // 2 - img_b.get_width() // 2
    screen.blit(img_b, (xb, 20))

    # white - at the very bottom, centered
    cw = int(time_w)
    text_w = f"{cw // 60}:{cw % 60:02d}"
    img_w = font.render(text_w, True, (255, 255, 255))
    xw = BOARD + PANEL // 2 - img_w.get_width() // 2
    yw = HEIGHT - 20 - img_w.get_height()
    screen.blit(img_w, (xw, yw))

    # Restart - vertically centered in the panel
    pygame.draw.rect(screen, (70, 70, 70), restart_btn)
    text_btn = small_font.render("Restart", True, (255, 255, 255))
    tx = restart_btn.centerx - text_btn.get_width() // 2
    ty = restart_btn.centery - text_btn.get_height() // 2
    screen.blit(text_btn, (tx, ty))

board = new_board()
game_started = False   # the clock runs only after the first move
time_w = 600.0     # white - 10 minutes in seconds
time_b = 600.0     # black - 10 minutes in seconds
running = True
selected = None
turn = "w"         # white starts
en_passant_target = None
white_king_moved = False
black_king_moved = False
rook_moved = {
    (7, 0): False,   # white rook left (queenside)
    (7, 7): False,   # white rook right (kingside)
    (0, 0): False,   # black rook left
    (0, 7): False,   # black rook right
}
game_over = None   # None while the game runs; holds the result text when it ends
restart_btn = pygame.Rect(BOARD + PANEL // 2 - 80, HEIGHT // 2 - 25, 160, 50)

while running:
    ms = clock.tick(60)
    seconds = ms / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if restart_btn.collidepoint(mx, my):
                board = new_board()
                turn = "w"
                selected = None
                game_over = None
                game_started = False
                time_w = 600.0
                time_b = 600.0
            elif game_over is None:
                col = mx // SQUARE
                row = my // SQUARE
                if row < 8 and col < 8:
                    if selected is None:
                        clicked = board[row][col]
                        if clicked != ".":
                            if clicked.isupper():
                                piece_color = "w"
                            else:
                                piece_color = "b"
                            if piece_color == turn:
                                selected = (row, col)
                    else:
                        old_row, old_col = selected
                        piece = board[old_row][old_col]
                        if piece.lower() == "k" and old_row == row and abs(col - old_col) == 2 and is_castling_possible(board, turn, old_row, old_col, col, white_king_moved, black_king_moved, rook_moved):
                            # move the king
                            board[row][col] = piece
                            board[old_row][old_col] = "."
                            game_started = True
                            # move the rook depending on side
                            if col == 6:
                                board[row][5] = board[row][7]
                                board[row][7] = "."
                            else:
                                board[row][3] = board[row][0]
                                board[row][0] = "."
                            # king has moved
                            en_passant_target = None
                            if turn == "w":
                                white_king_moved = True
                            else:
                                black_king_moved = True
                            selected = None
                            # switch player + check for mate
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            if not has_legal_move(board, turn):
                                if is_check(board, turn):
                                    game_over = "CHECKMATE - " + ("black" if turn == "w" else "white") + " wins"
                                else:
                                    game_over = "STALEMATE - draw"

                        elif piece.lower() == "p" and en_passant_target is not None and (row, col) == en_passant_target:
                            # move your pawn to the target (empty square)
                            board[row][col] = piece
                            board[old_row][old_col] = "."
                            game_started = True
                            board[old_row][col] = "."   # capture the enemy pawn beside your start
                            en_passant_target = None
                            selected = None
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            if not has_legal_move(board, turn):
                                if is_check(board, turn):
                                    game_over = "CHECKMATE - " + ("black" if turn == "w" else "white") + " wins"
                                else:
                                    game_over = "STALEMATE - draw"

                        elif is_move_valid(board, piece, old_row, old_col, row, col) and not leaves_king_in_check(board, turn, old_row, old_col, row, col):
                            board[row][col] = piece
                            board[old_row][old_col] = "."
                            game_started = True
                            if piece == "P" and row == 0:
                                board[row][col] = "Q"
                            if piece == "p" and row == 7:
                                board[row][col] = "q"
                            if piece == "K":
                                white_king_moved = True
                            if piece == "k":
                                black_king_moved = True
                            if (old_row, old_col) in rook_moved:
                                rook_moved[(old_row, old_col)] = True
                            if piece.lower() == "p" and abs(row - old_row) == 2:
                                en_passant_target = ((row + old_row) // 2, col)
                            else:
                                en_passant_target = None
                            selected = None
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            if not has_legal_move(board, turn):
                                if is_check(board, turn):
                                    game_over = "CHECKMATE - " + ("black" if turn == "w" else "white") + " wins"
                                else:
                                    game_over = "STALEMATE - draw"
                        else:
                            selected = None

    draw_board()
    pygame.draw.rect(screen, (50, 50, 55), (BOARD, 0, PANEL, HEIGHT))
    draw_clock()
    if turn == "w":
        title = "Turn: white"
    else:
        title = "Turn: black"
    if game_over is None and game_started:
        if turn == "w":
            time_w = time_w - seconds
        else:
            time_b = time_b - seconds
        if time_w <= 0:
            game_over = "TIME OUT - black wins"
        if time_b <= 0:
            game_over = "TIME OUT - white wins"
    pygame.display.set_caption(title)
    draw_check()
    draw_turn()
    draw_moves()
    draw_pieces()
    draw_selection()
    draw_end()

    pygame.display.flip()

pygame.quit()
