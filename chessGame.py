import pygame
import sys
import chess
import chess.svg
from pygame.locals import QUIT, MOUSEBUTTONDOWN
# from playsound import playsound

# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = min(WIDTH, HEIGHT)
SQUARE_SIZE = BOARD_SIZE // 8
LIGHT_COLOR = (150, 150, 200)
LIGHT_SELECTED_COLOR = (74,181,106)

DARK_COLOR = (100, 100, 150)
DARK_SELECTED_COLOR = (49,157,81)

TRIANGLE_SIZE = 20

class Game():
    def __init__(self,board,FPS=30):
        self.board = board
        self.FPS = FPS
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.pieces = {}
        self.colorAndSquares = []

        self.init_pygame
        self.init_pieces()
        self.init_squares()

    # initialtise pygame elements 
    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Chess Game')
        


    # initialise piece svg dictionary
    def init_pieces(self):
        for color in ['w', 'b']:
            for piece in ['r', 'n', 'b', 'q', 'k', 'p']:
                img = pygame.image.load(f'./media/{color}{piece}.svg')
                img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                self.pieces[f'{color}{piece}'] = img

    # initialise all the square
    # (useful for highlighting certain squares)
    def init_squares(self):
        for row in reversed(range(8)):
            for col in range(8):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                self.colorAndSquares.append([color,pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),False])
    


    def draw_board(self):
            for color, square, selected in self.colorAndSquares:
                pygame.draw.rect(self.screen, color, square)
                if selected:
                    self.draw_square_with_triangles(color,*square)


    # Draw triangles in the corners
    # used when a piece is capturable
    def draw_square_with_triangles(self,color,x, y, w, h):
        pygame.draw.polygon(self.screen, (color[0],200,color[2]), [(x, y), (x + TRIANGLE_SIZE, y), (x, y + TRIANGLE_SIZE)])
        pygame.draw.polygon(self.screen, (color[0],200,color[2]), [(x + w, y), (x + w - TRIANGLE_SIZE, y), (x + w, y + TRIANGLE_SIZE)])
        pygame.draw.polygon(self.screen, (color[0],200,color[2]), [(x, y + h), (x + TRIANGLE_SIZE, y + h), (x, y + h - TRIANGLE_SIZE)])
        pygame.draw.polygon(self.screen, (color[0],200,color[2]), [(x + w, y + h), (x + w - TRIANGLE_SIZE, y + h), (x + w, y + h - TRIANGLE_SIZE)])




        

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                piece = piece.symbol()
                key = "w"+piece.lower() if piece.isupper() else "b"+piece
                img = self.pieces[key]
                x = (chess.square_file(square) * SQUARE_SIZE) + (SQUARE_SIZE // 2)
                y = HEIGHT - ((chess.square_rank(square) + 1) * SQUARE_SIZE) + (SQUARE_SIZE // 2)
                self.screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))


    def getSquare(self,x,y):
        col = x // SQUARE_SIZE
        row = 7 - (y // SQUARE_SIZE)  
        return chess.square(col, row)
    

    def highlightSquares(self,squares):
        for i,square in enumerate(self.colorAndSquares):
            square[0] = LIGHT_COLOR if ((i%8) + (i//8)) % 2 == 1 else DARK_COLOR
            square[2] = False
            if i in squares:
                if self.board.piece_at(i) is not None and self.board.piece_at(i).color is not self.board.turn:
                    square[2] = True
                else:
                    if square[0] is LIGHT_COLOR:
                            square[0] = LIGHT_SELECTED_COLOR
                    else:
                        square[0] = DARK_SELECTED_COLOR

                    


    def selectSquare(self,chosenSquare):
        allMoves = list(self.board.legal_moves)
        possibleMoves = [move for move in allMoves if move.from_square==chosenSquare]
        self.highlightSquares([toSquare.to_square for toSquare in possibleMoves])

    def movePiece(self,squareFrom,squareTo):
        if self.board.piece_at(squareFrom) == chess.Piece(chess.PAWN,self.board.turn) and ((chess.square_rank(squareFrom) == 1 and not self.board.turn) or (chess.square_rank(squareFrom) == 6 and self.board.turn)):
            self.board.push(chess.Move(squareFrom,squareTo,promotion=chess.QUEEN))
            self.highlightSquares([])
            squareFrom = None
        else:
            self.board.push(chess.Move(squareFrom,squareTo))
            self.highlightSquares([])
            squareFrom = None

    def handleClick(self,chosenSquare):

        x, y = pygame.mouse.get_pos()
        square = self.getSquare(x,y)

        # square hasn't been chosen yet
        if chosenSquare == None:
            chosenSquare = square
            self.selectSquare(chosenSquare)
        
        # square has been chosen
        else:
            # check if another friendly piece has been chosen
            if self.board.piece_at(square) is not None and self.board.piece_at(square).color == self.board.turn:
                if square == chosenSquare:
                    self.highlightSquares([])
                    chosenSquare = None

                else:
                    chosenSquare = square
                    self.selectSquare(chosenSquare)

            # check if valid move has been chosen
            elif any(move.from_square == chosenSquare and move.to_square == square for move in self.board.legal_moves):
                self.movePiece(chosenSquare,square)


            # set chosenSquare to None
            else:
                chosenSquare = None
                self.highlightSquares([])

        return chosenSquare

    def draw_all(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def main(self):
        chosenSquare = None
        while True:
            if self.board.is_checkmate():
                    print("game over")
                    break
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    chosenSquare = self.handleClick(chosenSquare)
     
            self.draw_all()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    board = chess.Board()
    game = Game(board)
    game.main()