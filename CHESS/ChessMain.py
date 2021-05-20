"""
This is our Main driver file. it will deal with user input and displaying current game state.it will also be responsible
 for determining the valid moves at the current game state.It will also keep a move log.
"""

from __future__ import division  # needed that for animation
import pygame as p
from CHESS import ChessEngine, ChessAI


BOARD_WIDTH = BOARD_HEIGHT = 512   # 400 is another possibility
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # dimension of chess board are 8*8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
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
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT)) # add move log panel width
    clock = p.time.Clock()  # no use yet
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveLogFont = p.font.SysFont("Arial", 14, True, False)
    moveMade = False  # flag variable
    animate = False  # flag variable
    loadImages()  # only doing this once before the while loop
    sqSelected = ()  # keep track of the square selected by the player (no square selected currently)
    playerClicks = []  # keep track of both of the square selected by the user ( list of SqSelected)
    gameOver = False
    running = True
    playerOne = False   # if a Human is playing white, then this will be True. if an Ai is Playing, then False
    playerTwo = False    # same as above but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # x and y coordinate of mouse pointer
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    #print("row, col: " ,row, col)  # for now ------
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()  # deselect th selected square
                        playerClicks = []  # clear player selects
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both first and second player clicks
                        if len(playerClicks) == 2:  # after second move
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            # print(move.getChessNotation()) uncomment it later

                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                                if not moveMade:
                                    playerClicks = [sqSelected]

            # key handler
            elif e.type == p.KEYDOWN:

                if e.key == p.K_z:  # UNDO when z is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                if e.key == p.K_r:  # RESET the board when key 'k' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        # To Check if checkmate or stalemate self

        if not validMoves:
            if gs.underCheck():
                gs.checkmate = True
            else:
                gs.stalemate = True

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Black wins by CheckMate' if gs.whiteToMove
            else'White wins by Checkmate')

        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics within a current Game state.
'''

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # draws square on the board
    highlightSquares(screen, gs,validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of these squares

    drawMoveLog(screen, gs, moveLogFont)


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
Highlights square selected and moves the piece selected 
'''

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected has a piece that could be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value 0-> transparent; 255-> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from tht square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


'''
Draw the pieces on the board using the current Game state.board
'''

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # square is not empty.
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
renders the move text
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("yellow"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + " "
        if i+1 < len(moveLog):  # make sure black made a move
            moveString += moveLog[i+1].getChessNotation() + " "
        moveTexts.append(moveString)

    movesPerRow = 2
    padding = 5
    lineSpacing = 4
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    colors = [p.Color("white"), p.Color("grey")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        frameValue = frame/frameCount
        r, c = (move.startRow + dR * frameValue, move.startCol + dC * frameValue)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece move from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.enPassant:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(70)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, False, p.Color('Gray'))
    textLocation = p.Rect(False, False, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2,
                                                            BOARD_HEIGHT / 2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    main()
