# Python Chess Game

A fully playable two-player chess game built from scratch in Python with PyGame. It implements the complete rules of chess, a clickable board, move highlighting, a game clock, and a side panel - all rendered with sharp vector piece graphics.

This was written step by step as a learning project. The code is intentionally kept explicit and readable rather than clever, so it doubles as a walkthrough of how a chess engine's rules can be built up piece by piece.

> A Slovak-commented version of the source is also available in this repository.

## Features

### Core gameplay
- **8x8 board** rendered with alternating light/dark squares.
- **Click-to-move**: click a piece to select it, click a destination to move. Pixel coordinates are converted to board squares.
- **Move highlighting**: when a piece is selected, all of its legal destination squares are highlighted in translucent green.
- **Turn enforcement**: players alternate; you can only select and move pieces of the color whose turn it is. The side to move is shown by a green bar (bottom for white, top for black) and in the window title.

### Full movement rules
Every piece follows correct chess movement, validated in `is_move_valid`:
- **Rook** - horizontal and vertical lines.
- **Bishop** - diagonals.
- **Queen** - rook + bishop combined.
- **Knight** - L-shaped jumps (can leap over pieces).
- **King** - one square in any direction.
- **Pawn** - forward one, initial two-square advance, diagonal capture, all direction-aware by color.
- **Path blocking** (`is_path_clear`) - rooks, bishops and queens cannot jump over pieces; the pawn's two-square advance is also blocked if a piece stands in the way.

### Check, checkmate and stalemate
- **Check detection** (`is_check`) - determines whether a king is attacked by asking whether any enemy piece has a valid move onto the king's square.
- **Illegal move prevention** (`leaves_king_in_check`) - a move is rejected if it would leave (or place) your own king in check. This is done by making the move on a temporary basis, testing for check, and undoing it.
- **Checkmate / stalemate** (`has_legal_move`) - after every move the program checks whether the side to move has any legal reply. No legal moves + in check = checkmate; no legal moves + not in check = stalemate.

### Special moves
- **Castling** (`is_castling_possible`) - both kingside and queenside, with all five conditions verified: king hasn't moved, rook hasn't moved (and is still there), squares between are empty, king isn't currently in check, and the king doesn't pass through or land on an attacked square. Move history is tracked with `white_king_moved`, `black_king_moved` and a `rook_moved` dictionary.
- **En passant** - a pawn that has just advanced two squares can be captured "in passing" on the very next move. The target square is remembered in `en_passant_target` and cleared after one move.
- **Pawn promotion** - a pawn reaching the far rank is automatically promoted to a queen.

### Game clock and side panel
- **10-minute clock per player**, counting down only for the side to move.
- The clock starts on the **first move**, not when the window opens.
- Time is displayed as `M:SS` in a **side panel** to the right of the board (black's clock at the top, white's at the bottom).
- Running out of time ends the game.

### End-of-game screen
- A translucent banner across the board announces the result (checkmate, stalemate or time out).
- A **Restart** button in the panel resets the board, clocks and all state at any time.

## Screenshots

*(Add your own screenshots here, e.g. `![Board](screenshots/board.png)`)*

## Requirements

- Python 3.x
- [pygame-ce](https://pyga.me/) (the Community Edition - it supports newer Python versions and the `load_sized_svg` function used to render sharp pieces)

```bash
python -m pip install pygame-ce
```

## Piece images

The game loads piece graphics from a `pieces/` folder (the Slovak version uses `figurky/`). It expects 12 SVG files named by color and piece:

```
pieces/
  wP.svg  wR.svg  wN.svg  wB.svg  wQ.svg  wK.svg
  bP.svg  bR.svg  bN.svg  bB.svg  bQ.svg  bK.svg
```

`w`/`b` = white/black, and the letter is the piece (P, R, N, B, Q, K). The images used are the free **cburnett** chess set (available on Wikimedia Commons / Lichess). Loading them with `load_sized_svg` renders the vectors sharply at any board size.

## How to run

1. Make sure the `pieces/` folder with the 12 SVG files sits next to `chess.py`.
2. Run:

```bash
python chess.py
```

## Controls

- **Click** a piece to select it, **click** a destination to move.
- Selecting the wrong-color piece or clicking the panel does nothing.
- Castle by moving the **king two squares** toward a rook.
- **Restart** button resets the game at any time.

## How the code is organized

Everything lives in a single file for simplicity. The main structure:

- **Setup** - constants (square size, board and panel dimensions, colors), fonts, window, and loading the piece images into a dictionary keyed by piece letter.
- **Drawing functions** - `draw_board`, `draw_pieces`, `draw_selection`, `draw_moves`, `draw_check`, `draw_turn`, `draw_clock`, `draw_end`.
- **Rule functions** - `is_path_clear`, `is_move_valid`, `is_check`, `leaves_king_in_check`, `has_legal_move`, `is_castling_possible`.
- **State** - the board (a list of lists), whose turn it is, selection, clocks, castling/en-passant tracking, and the game-over flag.
- **Main loop** - measures elapsed time, handles mouse clicks (selection, normal moves, castling, en passant), updates the clock, and redraws everything each frame.

The board is represented as a list of 8 lists of 8 characters. Uppercase letters are white pieces, lowercase are black, and `.` is an empty square.

## Possible future improvements

- Choice of promotion piece (not just queen)
- Move history / notation display in the panel
- A resizable window
- A simple computer opponent

## License

Free to use and modify. The cburnett piece images are licensed separately (see Wikimedia Commons).
