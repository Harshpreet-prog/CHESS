"""
This is our Main driver file. it will deal with user input and displaying current game state.it will also be responsible
 for determining the valid moves at the current game state.It will also keep a move log.
"""


import pygame as p
from CHESS import ChessEngine

WIDTH = HEIGHT = 600  # 400 is another possibility
DIMENSION = 8  # dimension of chess board are 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}

'''
Initialize a global dictionary of Images. This will be called exactly once in the main
'''


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


'''
The main driver for our code. this will handle user input and updating the graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable
    loadImages()  # only doing this once before the while loop
    sqSelected = ()  # keep track of the square selected by the player (no square selected currently)
    playerClicks = []  # keep track of both of the square selected by the user ( list of SqSelected)

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x and y coordinate of mouse pointer
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                print(row, col) # for now
                if sqSelected == (row, col):
                    sqSelected = ()  # deselect th selected square
                    playerClicks = []  # clear player selects
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both first and second player clicks
                    if len(playerClicks) == 2:  # after second move
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()  # clear for next move
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()  # FOR DEBUGGING UNORIGINAL
                    moveMade = False
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics within a current Game state.
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draws square on the board
    # add in piece highlighting or more suggestion (later)
    drawPieces(screen, gs.board)  # draw pieces on top of these squares


'''
Draw the squares on the board.(top left square always light)
'''


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current Game state.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # square is not empty.
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
