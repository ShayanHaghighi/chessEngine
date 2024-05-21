import time
import chess
import math
             # reverse index with black <---
pawnPST =  [0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0]

knightPST = [-66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69]

bishopPST = [-59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10]

rookPST = [  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32]

queenPST = [6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42]

kingPST = [4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18]

      


class MinMax():
    def __init__(self,game,weights):
        self.game = game
        self.transposition_table = {}
        self.weights = weights

    def reverseIndex(self,index):
        return 56 + (index%8)-(index//8)*8

    def simpleSumPieces(self,board):
        eval = 0
        pieceDict = board.piece_map()
        for position in board.piece_map():
            piece = pieceDict[position]
            
            val = 0
            if piece.piece_type==chess.PAWN:
                if piece.color:
                    val = 100+pawnPST[self.reverseIndex(position)]
                else:
                    val = -100-pawnPST[position]

            elif piece.piece_type==chess.KNIGHT:
                if piece.color:
                    val = 280+knightPST[self.reverseIndex(position)]
                else:
                    val = -280-knightPST[position]

            elif piece.piece_type==chess.BISHOP:
                if piece.color:
                    val = 320+bishopPST[self.reverseIndex(position)]
                else:
                    val = -320-bishopPST[position]

            elif piece.piece_type==chess.ROOK:
                if piece.color:
                    val = 470+rookPST[self.reverseIndex(position)]
                else:
                    val = -470-rookPST[position]

            elif piece.piece_type==chess.QUEEN:
                if piece.color:
                    val = 929+queenPST[self.reverseIndex(position)]
                else:
                    val = -929-queenPST[position]

            elif piece.piece_type==chess.KING:
                if piece.color:
                    val = kingPST[self.reverseIndex(position)]
                else:
                    val = -kingPST[position]

            eval += val
        return eval


    def order_moves(self, board):
            captures = []
            non_captures = []

            for move in board.legal_moves:
                if board.is_capture(move):
                    captures.append(move)
                else:
                    non_captures.append(move)
            
            captures.sort(key=lambda move: self.staticEval(board), reverse=True)
            return captures + non_captures

    # TODO
    # move ordering
    def staticEval(self,board):
        return self.simpleSumPieces(board)
    



    
    def minimax(self,board,depth,alpha,beta,maximisingPlayer):
        board_hash = hash(board.fen())

        if board_hash in self.transposition_table:
            stored_eval, stored_depth, eval_type, _ = self.transposition_table[board_hash]
            if stored_depth >= depth:
                if eval_type == 'EXACT':
                    return stored_eval, None
                elif eval_type == 'ALPHA' and stored_eval <= alpha:
                    return alpha, None
                elif eval_type == 'BETA' and stored_eval >= beta:
                    return beta, None


        
        if board.outcome():

            if board.outcome().termination==chess.Termination.CHECKMATE:
                if board.outcome().winner:
                    return 100000000-board.ply(), None
                else:
                    return -100000000+board.ply(), None
            elif board.outcome().termination.value>1:
                return 0,None

        if depth == 0:
            eval = self.staticEval(board)
            self.transposition_table[board_hash] = (eval, depth, 'EXACT', board.ply())
            return eval,None
        
        
            
        if maximisingPlayer:
            maxEval = -math.inf
            bestMove = None
            for move in self.order_moves(board):
                board.push(move)
                # self.game.draw_all()

                eval,_ = self.minimax(board,depth-1,alpha,beta,not maximisingPlayer)
                
                board.pop()
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move

                alpha = max(alpha,eval)
                if beta <= alpha:
                    break

            if maxEval <= alpha:
                eval_type = 'BETA'
            elif maxEval >= beta:
                eval_type = 'ALPHA'
            else:
                eval_type = 'EXACT'
            self.transposition_table[board_hash] = (maxEval, depth, eval_type, board.ply())

            return maxEval,bestMove
        
        if not maximisingPlayer:
            minEval = math.inf
            bestMove = None
            for move in self.order_moves(board):
                board.push(move)
                # self.game.draw_all()
                (eval,e) = self.minimax(board,depth-1,alpha,beta,not maximisingPlayer)
                board.pop()
                # print("eval:")
                # print(eval,e)
                if eval < minEval:
                    minEval = eval
                    bestMove = move

                beta = min(beta,eval)
                if beta <= alpha:
                    break
                
            if minEval <= alpha:
                eval_type = 'BETA'
            elif minEval >= beta:
                eval_type = 'ALPHA'
            else:
                eval_type = 'EXACT'
            self.transposition_table[board_hash] = (minEval, depth, eval_type, board.ply())

            return minEval,bestMove
        
    def iterative_deepening(self, board, max_depth,maximisingPlayer):
        self.transposition_table = {k: v for k, v in self.transposition_table.items() if v[3]<board.ply()}
        best_move = None
        # self.transposition_table = {}
        depth = 1
        # for depth in range(1, max_depth + 1):
        start = time.time()
        while depth < max_depth and time.time()-start < 2:
            eval, best_move = self.minimax(board, depth, -math.inf, math.inf, maximisingPlayer)
            depth += 1

        print("depth",depth)
        return eval,best_move 
    

# if __name__=="__main__":
#     ai = MinMax()
#     for i in range(64):
#         print(ai.reverseIndex(i))