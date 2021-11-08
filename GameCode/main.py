import pygame
from checkers.board import Board
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.minimax import getAllMoves, minimax
from checkers.pieces import Piece
FPS = 60

WHITE_DEPTH = 3
RED_DEPTH = 3

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def getRowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

if __name__ == '__main__':
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            print("White!")
            value, newBoard = minimax(game.getBoard(), WHITE_DEPTH, True, game)
            game.aiMove(newBoard)
        elif game.turn == RED:
            print("Red!")
            value, newBoard = minimax(game.getBoard(), RED_DEPTH, False, game)
            game.aiMove(newBoard)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update()
    
    pygame.quit()