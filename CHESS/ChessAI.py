import random

pieceScore = {'K': 0, 'Q': 10, 'B': 4, 'N': 3, 'R': 5, 'p': 1}  # king was originally set to 0
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

blackPawnScores = [
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [10, 10, 10, 10, 10, 10, 10, 10],
                  [10, 10, 20, 30, 30, 20, 10, 10],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [90, 90, 90, 90, 90, 90, 90, 90]]


whitePawnScores = [[90, 90, 90, 90, 90, 90, 90, 90],
                   [50, 50, 50, 50, 50, 50, 50, 50],
                   [10, 10, 20, 30, 30, 20, 10, 10],
                   [10, 10, 10, 10, 10, 10, 10, 10],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1]]

kingScores =    [[1, 4, 1, 1, 1, 1, 4, 5],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-2, -2, -13, -13, -13, -13, -2, -2],
                [-2 -3, -13, -40, -40, -13, -3, -2],
                [-2, -3, -13, -40, -40, -13, -3, -2],
                [-2, -2, -13, -13, -13, -13, -2, -2],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 4, 3, 1, 1, 1, 3, 4]]

queenScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

rookScores =   [[2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 3, 3, 3, 3, 2, 2],
                [2, 3, 3, 2, 2, 3, 3, 2],
                [2, 3, 3, 2, 2, 3, 3, 2],
                [2, 2, 3, 3, 3, 3, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2]]

bishopScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 1, 2, 2, 1, 3, 1],
                [1, 2, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 1, 2, 2, 1, 3, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]




piecePositionalScores = {"N" : knightScores, "R" : rookScores, "K" : kingScores, "B" : bishopScores, "Q": queenScores, "bp" : blackPawnScores, "wp": whitePawnScores}

def findRandomMove(validMoves):
    if validMoves:
        return validMoves[random.randint(0, len(validMoves)-1)]

'''
Helper method to make first recursive call
'''

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove


def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            gs.getValidMoves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    print("yes")
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  #pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # black win
        else:
            return CHECKMATE  # white win
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            piecePositionScore = 0
            if square != "--":
                # score it positionally

                if square[1] == "N":
                    piecePositionScore = piecePositionalScores["N"][row][col]

                if square[1] == "K":
                    piecePositionScore = piecePositionalScores["K"][row][col]

                if square[1] == "B":
                    piecePositionScore = piecePositionalScores["B"][row][col]

                if square[1] == "Q":
                    piecePositionScore = piecePositionalScores["Q"][row][col]

                if square[1] == "R":
                    piecePositionScore = piecePositionalScores["R"][row][col]

                if square == "bp":
                    piecePositionScore = piecePositionalScores["bp"][row][col]

                if square[1] == "wp":
                    piecePositionScore = piecePositionalScores["wp"][row][col]

            if square[0] == 'w':
                score += pieceScore[square[1]] + (piecePositionScore * 0.1)
            elif square[0] == 'b':
                score -= pieceScore[square[1]] + (piecePositionScore * 0.1)

    return score

'''
Score the board based on material
'''

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score