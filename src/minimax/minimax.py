from copy import deepcopy
import pygame

from checkers.pieces import Piece

RED = (255,0,0)
WHITE = (255,255,255)

def minimax(position, depth, maxPlayer, game,alpha=100,beta=-100):
    if depth==0:
        return position.evaluate(),position
    if position.winner():
        return position.evaluate(),position
    if maxPlayer:
        color=WHITE
    else:
        color=RED
    moveVal={}
    nextAlpha=alpha
    nextBeta=beta
    allMoves=getAllMoves(position,color)
    for member in allMoves:
        piece=member[0]
        for move in member[1]:
            #print(piece.row,piece.col)
            newPosition=simulateMove(deepcopy(piece),move,deepcopy(position),game)
            #print(move,piece.row,piece.col)
            val,_=minimax(newPosition,depth-1,not maxPlayer,game,nextAlpha,nextBeta)
            if game.hasSeen(newPosition):
                continue
            if color==RED and val<beta:
                return val,newPosition
            if color==WHITE and val>nextBeta:
                nextBeta=val
            if color==WHITE and val>alpha:
                return val,newPosition
            if color==RED and val<nextAlpha:
                nextAlpha=val
            moveVal[newPosition]=val
    if len(moveVal)==0:
            return position.evaluate(),position
    if maxPlayer:
        maxKey=max(moveVal,key=moveVal.get)
        #print(moveVal[maxKey])
        return moveVal[maxKey],maxKey
    else:
        minKey=min(moveVal,key=moveVal.get)
        #print(moveVal[minKey])
        return moveVal[minKey],minKey

def simulateMove(piece, move, board, game, skip=[]):
    piece=board.getPiece(piece.row,piece.col)
    board.move(piece,move[0],move[1])
    for skipped in move[2]:
        board.remove([board.getPiece(skipped.row,skipped.col)])
        #board.move(piece,piece.row+2*move[0],piece.col+2*move[1])
    return board

def getAllMoves(board, color, game=0):
    moves=[];
    pieces=board.getAllPieces(color)
    for piece in pieces:
        pieceMoves=board.getValidMoves(piece)
        if(len(pieceMoves)>0):
            moves.append((piece,pieceMoves))
    #print(moves)
    return moves