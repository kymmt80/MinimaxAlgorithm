import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:

    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        #for _ in range(100000000):
        #    pass
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.validMoves = {}
        self.last64=[]
        self.turns=0

    def winner(self):
        return self.board.winner()

    def _move(self, row, col):
        piece = self.board.getPiece(row, col)
        if self.selected and piece == 0 and (row, col) in self.validMoves:
            self.board.move(self.selected, row, col)
            skipped = self.validMoves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.changeTurn()
        else:
            return False
        return True

    def changeTurn(self):
        self.validMoves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def getBoard(self):
        return self.board

    def aiMove(self, board):
        self.board = board
        self.changeTurn()
        self.addLast(board)
        self.turns+=1
    
    def addLast(self,position):
        if len(self.last64)<64:
            self.last64.append(position)
        else:
            self.last64[self.turns%64]=position

    def hasSeen(self,position):
        for board in self.last64:
            equal=True
            for i in range(8):
                for j in range(8):
                    if board.board[i][j]==position.board[i][j] and board.board[i][j]==0:
                        continue
                    if board.board[i][j]==0 or position.board[i][j] ==0:
                        equal=False
                        break
                    if board.board[i][j].color==position.board[i][j].color:
                        continue
                    equal=False
                    break
                if not equal:
                    break
            if equal:
                return True
        return False
