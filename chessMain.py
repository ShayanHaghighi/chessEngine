from chessGame import Game
import chess
import pygame
from pygame.locals import *
import sys
from minimax import MinMax 
import math
import time
from stockfish import Stockfish


stockfish = Stockfish()

board = chess.Board()
game = Game(board)
ai = MinMax(game,[1,1,1,1,1,1])

DEPTH = 4

def main(game):
    chosenSquare = None
    while True:
        if board.outcome():
                print("game over")
                print(board.outcome())
                return board.outcome()
        

        if not board.turn:
            start = time.time()
            eval,move = ai.iterative_deepening(board,DEPTH,False)
            print("final eval:")
            print(eval,move)
            if not move:
                 time.sleep(5000)
            board.push(move)
            print(time.time()-start)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                chosenSquare = game.handleClick(chosenSquare)
    
        game.draw_all()
        game.clock.tick(game.FPS)

main(game)

