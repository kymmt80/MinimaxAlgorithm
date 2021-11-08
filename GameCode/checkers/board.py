from copy import deepcopy
from typing import Collection
import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .pieces import Piece

class Board:
    	
    def __init__(self):
        self.board = []
        self.redLeft = self.whiteLeft = 12
        self.redKings = self.whiteKings = 0
        self.createBoard()
    
    def drawSquares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.whiteLeft - self.redLeft + (self.whiteKings * 2 - self.redKings * 2)

    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.makeKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.redKings += 1 

    def getPiece(self, row, col):
        return self.board[row][col]

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.drawSquares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.redLeft -= 1
                else:
                    self.whiteLeft -= 1
    
    def winner(self):
        if self.redLeft <= 0:
            return WHITE
        elif self.whiteLeft <= 0:
            return RED
        
        return None 
    
    def getValidMoves(self, piece,skipped=[]):
        #print("*",piece.color,piece.row,piece.col)
        #print("*",skipped)
        validMoves=[]
        if(piece.color==RED):
            a=-1
        else:
            a=1
        moves={(1,1),(1,-1),(-1,-1),(-1,1)}
        kingMoves={(-1,-1),(-1,1)}
        for move in moves:
            move_skipped=[]
            x,y=piece.row,piece.col
            x+=a*move[0]
            y+=a*move[1]
            if(y<0 or y>=COLS or x>=ROWS or x<0):
                continue
            if(move in kingMoves) and not piece.king:
                continue
            if self.board[x][y]==0:
                if len(skipped)==0:
                    validMoves.append((x,y,[]))
                else:
                    continue
            elif self.board[x][y].color!=piece.color and not (y+a*move[1]<0 or y+a*move[1]>=COLS or x+a*move[0]>=ROWS or x+a*move[0]<0):
                if self.board[x+a*move[0]][y+a*move[1]]==0:
                    if True in ((skip.row==x and skip.col==y) for skip in skipped):
                       continue
                    move_skipped.append(self.getPiece(x,y))
                    validMoves.append((x+move[0]*a,y+move[1]*a,skipped+move_skipped))
                    simPiece=Piece(x+move[0]*a,y+move[1]*a,piece.color)
                    simPiece.king=piece.king
                    #print(piece.color,piece.row,piece.col,"before:",validMoves)
                    validMoves=validMoves+self.getValidMoves(simPiece,skipped+move_skipped)
                    #print(piece.color,piece.row,piece.col,"after:",validMoves)
            #print(piece.color,piece.row,piece.col)
            #print(validMoves)
        return validMoves
        


    def _traverseLeft(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverseLeft(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverseRight(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverseRight(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverseLeft(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverseRight(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves