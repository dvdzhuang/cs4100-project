import chess

count = 0

class ChessGameState:
    def __init__(self, board=chess.Board()):
        self.board = board

    def getLegalActions(self):
        return [x for x in self.board.legal_moves]

    def generateSuccessor(self, action):
        global count
        count += 1
        self.board.push(action)
        rep = self.board.fen()
        self.board.pop()
        return ChessGameState(chess.Board(rep))

    def getTurn(self):
        return 'White' if self.board.turn else 'Black'

    def isEnd(self):
        return self.board.is_checkmate() or self.board.is_stalemate()

    def getBoard(self):
        return self.board

    def getFEN(self):
        return self.board.fen()

    def getCount(self):
        global count
        return count

#test = chess.Board()
#model = ChessGameState(test)
#next = model.generateSuccessor(chess.Move.from_uci('a2a3'))
#print(model.getLegalActions())