"""
This class is responsible for Storing all the information about the current state of a chess game
"""


class GameState():
    def __init__(self):
        # board is an 8*8 2d list, each element of the list has 2 characters.
        # the first character represents the color of the piece, 'b' or 'w'.
        # the second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    '''
    Takes move as an parameter and performs it
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move for other applications
        self.whiteToMove = not self.whiteToMove  # swap the players
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # print(self.whiteToMove)

    '''
        undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    all moves considering checks
    '''

    def getValidMoves(self):

        # 1.Generate all possible moves
        moves = self.getAllPossibleMoves()

        # 2. For each move,make the move
        for i in range(len(moves)-1, -1, -1):  # Always check the list in reverse when removing a element from it.
            self.makeMove(moves[i])
            # 3.generate all opponent's moves
            # 4.for each of your opponent moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  # 5.remove the move which attacks your king
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    '''
    Check if the player is in check
    '''

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        pass

    '''
    Determine if the square is being attacked
    '''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()

        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    '''
    all moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # noinspection PyArgumentList
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate function based on piece type
        return moves

    '''
    get all the possible moves for the piece and add these 'moves' to the list moves
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == '--':  # one square pawn push
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':  # two square pawn push
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # left piece capture
                if self.board[r - 1][c - 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # right piece capture
                if self.board[r - 1][c + 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == '--':  # one square pawn push
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':  # two square pawn push
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # left piece capture
                if self.board[r + 1][c - 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # right piece capture
                if self.board[r + 1][c + 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
        get all the possible moves for the piece and add these 'moves' to the list moves
    '''

    def getRookMoves(self, r, c, moves):
        # print(r, c)
        for i in reversed(range(c)):  # LEFT
            if self.board[r][i] == "--":
                moves.append(Move((r, c), (r, i), self.board))
            elif self.board[r][i] != "--":
                if (self.board[r][i][0] == "b" and self.whiteToMove) \
                        or (self.board[r][i][0] == "w" and not self.whiteToMove):
                    moves.append(Move((r, c), (r, i), self.board))
                    break
                else:  # friend
                    break
        for j in range(c + 1, 8):  # RIGHT MOVEMENT
            if self.board[r][j] == "--":
                moves.append(Move((r, c), (r, j), self.board))
            elif self.board[r][j] != "--":
                print((r, c), (r, j))
                if (self.board[r][j][0] == "b" and self.whiteToMove) \
                        or (self.board[r][j][0] == "w" and not self.whiteToMove):
                    moves.append(Move((r, c), (r, j), self.board))
                    print((r, c), (r, j))
                    break
                else:  # friend
                    break
        for i in reversed(range(r)):  # UP MOVEMENT
            if self.board[i][c] == "--":
                moves.append(Move((r, c), (i, c), self.board))
            elif self.board[i][c] != "--":
                if (self.board[i][c][0] == "b" and self.whiteToMove) \
                        or (self.board[i][c][0] == "w" and not self.whiteToMove):
                    moves.append(Move((r, c), (i, c), self.board))
                    break
                else:  # friend
                    break
        for j in range(r + 1, 8):  # DOWN MOVEMENT

            if self.board[j][c] == "--":
                moves.append(Move((r, c), (j, c), self.board))
            elif self.board[j][c] != "--":
                if (self.board[j][c][0] == "b" and self.whiteToMove) \
                        or (self.board[j][c][0] == "w" and not self.whiteToMove):
                    moves.append(Move((r, c), (j, c), self.board))
                    break
                else:  # friend
                    break

    '''
          get all the possible moves for the knight and add these 'moves' to the list moves
    '''

    def getKnightMoves(self, r, c, moves):
        # FOR ALONG ROW MOVEMENT
        if(r + 2) in range(0, 8):
            if (c - 1) in range(0, 8):                                  # LEFT TO THE SQUARE r + 2
                if self.board[r + 2][c - 1] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
                elif (self.board[r + 2][c - 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 2][c - 1][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if (c + 1) in range(0, 8):                                  # RIGHT TO THE SQUARE r + 2
                if self.board[r + 2][c + 1] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
                elif (self.board[r + 2][c + 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 2][c + 1][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))

        if (r - 2) in range(0, 8):
            if (c - 1) in range(0, 8):                                  # LEFT TO THE SQUARE r - 2
                if self.board[r - 2][c - 1] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
                elif (self.board[r - 2][c - 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 2][c - 1][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if (c + 1) in range(0, 8):                                  # RIGHT TO THE SQUARE r - 2
                if self.board[r - 2][c + 1] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
                elif (self.board[r - 2][c + 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 2][c + 1][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))

        # FOR ALONG COLUMN MOVEMENT
        if (c + 2) in range(0, 8):
            if (r - 1) in range(0, 8):                                  # UP TO THE SQUARE c + 2
                if self.board[r - 1][c + 2] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
                elif (self.board[r - 1][c + 2][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 1][c + 2][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if (r + 1) in range(0, 8):                                  # DOWN TO THE SQUARE c + 2
                if self.board[r + 1][c + 2] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
                elif (self.board[r + 1][c + 2][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 1][c + 2][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))

        if (c - 2) in range(0, 8):
            if (r - 1) in range(0, 8):                                  # UP TO THE SQUARE c - 2
                if self.board[r - 1][c - 2] == "--":                    # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
                elif (self.board[r - 1][c - 2][0] == "b" and self.whiteToMove)\
                        or (self.board[r - 1][c - 2][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            if (r + 1) in range(0, 8):                                 # DOWN TO THE SQUARE c + 2
                if self.board[r + 1][c - 2] == "--":                   # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
                elif (self.board[r + 1][c - 2][0] == "b" and self.whiteToMove)\
                        or (self.board[r + 1][c - 2][0] == "w" and not self.whiteToMove):  # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))

    '''
          get all the possible moves for the Bishop and add these 'moves' to the list moves
    '''

    def getBishopMoves(self, r, c, moves):
        for i in range(1, 8):
            if (r - i) in range(0, 8) and (c + i) in range(0, 8):
                if self.board[r - i][c + i] == "--":                     # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - i, c + i), self.board))
                elif self.board[r - i][c + i] != "--":                   # SQUARE IS NOT EMPTY
                    if (self.board[r - i][c + i][0] == "b" and self.whiteToMove) \
                            or (self.board[r - i][c + i][0] == "w" and not self.whiteToMove):   # ENEMY PIECE TO CAPTURE
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                        break
                    else:                                                                       # FRIENDLY PIECE
                        break
        for j in range(1, 8):
            if (r - j) in range(0, 8) and (c - j) in range(0, 8):
                if self.board[r - j][c - j] == "--":                     # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - j, c - j), self.board))
                elif self.board[r - j][c - j] != "--":                   # SQUARE IS NOT EMPTY
                    if (self.board[r - j][c - j][0] == "b" and self.whiteToMove) \
                            or (self.board[r - j][c - j][0] == "w" and not self.whiteToMove):   # ENEMY PIECE TO CAPTURE
                        moves.append(Move((r, c), (r - j, c - j), self.board))
                        break
                    else:                                                # FRIENDLY PIECE
                        break

        for k in range(1, 8):
            if (r + k) in range(0, 8) and (c - k) in range(0, 8):
                if self.board[r + k][c - k] == "--":                     # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + k, c - k), self.board))
                elif self.board[r + k][c - k] != "--":                   # SQUARE IS NOT EMPTY
                    if (self.board[r + k][c - k][0] == "b" and self.whiteToMove) \
                            or (self.board[r + k][c - k][0] == "w" and not self.whiteToMove):   # ENEMY PIECE TO CAPTURE
                        moves.append(Move((r, c), (r + k, c - k), self.board))
                        break
                    else:                                                # FRIENDLY PIECE
                        break

        for h in range(1, 8):
            if (r + h) in range(0, 8) and (c + h) in range(0, 8):
                if self.board[r + h][c + h] == "--":                     # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + h, c + h), self.board))
                elif self.board[r + h][c + h] != "--":                   # SQUARE IS NOT EMPTY
                    if (self.board[r + h][c+h][0] == "b" and self.whiteToMove) \
                            or (self.board[r + h][c + h][0] == "w" and not self.whiteToMove):   # ENEMY PIECE TO CAPTURE
                        moves.append(Move((r, c), (r + h, c + h), self.board))
                        break
                    else:                                                                       # FRIENDLY PIECE
                        break

    '''
          get all the possible moves for the queen and add these 'moves' to the list moves
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
          get all the possible moves for the King and add these 'moves' to the list moves
    '''

    def getKingMoves(self, r, c, moves):
        # FOR SAME ROW MOVEMENT:
        if (c - 1) in range(0, 8):
            if self.board[r][c - 1] == "--":                      # SQUARE IS EMPTY
                moves.append(Move((r, c), (r, c - 1), self.board))
            elif (self.board[r][c - 1][0] == "b" and self.whiteToMove) \
                    or (self.board[r][c - 1][0] == "w" and not self.whiteToMove):             # ENEMY PIECE TO CAPTURE
                moves.append(Move((r, c), (r, c - 1), self.board))
        if (c + 1) in range(0, 8):
            if self.board[r][c + 1] == "--":                      # SQUARE IS EMPTY
                moves.append(Move((r, c), (r, c + 1), self.board))
            elif (self.board[r][c + 1][0] == "b" and self.whiteToMove) \
                    or (self.board[r][c + 1][0] == "w" and not self.whiteToMove):             # ENEMY PIECE TO CAPTURE
                moves.append(Move((r, c), (r, c + 1), self.board))
        # FOR DOWN THE ROW MOVEMENT:
        if (r + 1) in range(0, 8):
            if (c - 1) in range(0, 8):
                if self.board[r + 1][c - 1] == "--":             # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (self.board[r + 1][c - 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 1][c - 1][0] == "w" and not self.whiteToMove):    # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if (c + 1) in range(0, 8):
                if self.board[r + 1][c + 1] == "--":             # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (self.board[r + 1][c + 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 1][c + 1][0] == "w" and not self.whiteToMove):    # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if c in range(0, 8):
                if self.board[r + 1][c] == "--":                 # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r + 1, c), self.board))
                elif (self.board[r + 1][c][0] == "b" and self.whiteToMove) \
                        or (self.board[r + 1][c][0] == "w" and not self.whiteToMove):        # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r + 1, c), self.board))
        # FOR UP THE ROW MOVEMENT:
        if (r - 1) in range(0, 8):
            if (c - 1) in range(0, 8):
                if self.board[r - 1][c - 1] == "--":             # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (self.board[r - 1][c - 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 1][c - 1][0] == "w" and not self.whiteToMove):    # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if (c + 1) in range(0, 8):
                if self.board[r - 1][c + 1] == "--":             # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (self.board[r - 1][c + 1][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 1][c + 1][0] == "w" and not self.whiteToMove):    # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if c in range(0, 8):
                if self.board[r - 1][c] == "--":                 # SQUARE IS EMPTY
                    moves.append(Move((r, c), (r - 1, c), self.board))
                elif (self.board[r - 1][c][0] == "b" and self.whiteToMove) \
                        or (self.board[r - 1][c][0] == "w" and not self.whiteToMove):        # ENEMY PIECE TO CAPTURE
                    moves.append(Move((r, c), (r - 1, c), self.board))


class Move():
    #  maps keys to value
    #  key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals Method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add proper real notation logic later on
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
