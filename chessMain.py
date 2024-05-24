from chessGame import Game
from minimax import MinMax 
import chess
import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
import sys
import time

board = chess.Board()
game = Game(board)
ai = MinMax(game,[1,1,1,1,1,1])

DEPTH = 4
IS_BLACK_AI = True
IS_WHITE_AI = False

def play_move(isWhiteTurn):
    start = time.time()
    eval,move = ai.iterative_deepening(board,DEPTH,isWhiteTurn)
    print("final eval:")
    print(eval,move)
    board.push(move)
    print(time.time()-start)

def main(game):
    chosenSquare = None
    while True:
        
        # game is over
        if board.outcome():
                print("game over")
                print(board.outcome())
                return board.outcome()
        
        if not board.turn and IS_WHITE_AI:
            play_move(board.turn)

        if not board.turn and IS_BLACK_AI:
            play_move(board.turn)
            



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and not (IS_BLACK_AI and IS_WHITE_AI):
                chosenSquare = game.handleClick(chosenSquare)
    
        game.draw_all()
        game.clock.tick(game.FPS)

main(game)

