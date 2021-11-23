from model import ChessGameState
import chess


class Agent():
    def getAction(self, state):
        pass


def evalFunction(state):
    values = {
        'p': 1,
        'n': 3,
        'b': 3,
        'r': 5,
        'q': 9,
        'k': 0
    }
    colors = {
        True: 1,
        False: -1
    }
    board = state.getBoard()
    if board.is_checkmate():
        print('checkmate')
        print(board.fen)
        return -999999999999 * colors[board.turn]
    if board.is_stalemate():
        print('statemate')
        return 0
    total = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            piece_color = piece.color
            piece_symbol = piece.symbol()
            total += colors[piece_color] * values[piece_symbol.lower()]
    return total


class MinimaxAgent(Agent):

    def __init__(self, evalFn=evalFunction, depth=2):
        self.evaluationFunction = evalFn
        self.depth = depth

    def getAction(self, gameState):
        return max(gameState.getLegalActions(),
                   key=lambda x: self.getmin(gameState.generateSuccessor(x), self.depth))

    def getmin(self, state, depth):
        if state.isEnd():
            return self.evaluationFunction(state)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            scores.append(self.getmax(succ, depth - 1))
        return min(scores)

    def getmax(self, state, depth):
        if depth == 0 or state.isEnd():
            return self.evaluationFunction(state)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            scores.append(self.getmin(succ, depth))
        return max(scores)


class AlphaBetaAgent(Agent):
    def __init__(self, evalFn=evalFunction, depth=3):
        self.evaluationFunction = evalFn
        self.depth = depth

    def getAction(self, gameState):
        return max(gameState.getLegalActions(),
                   key=lambda x: self.getmin(gameState.generateSuccessor(x), self.depth,
                                             float('-inf'), float('inf')))

    def getmin(self, state, depth, alpha, beta):
        if state.isEnd():
            return self.evaluationFunction(state)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            v = self.getmax(succ, depth - 1, alpha, beta)
            if v <= alpha:
                return v
            beta = min(beta, v)
            scores.append(v)
        return min(scores)

    def getmax(self, state, depth, alpha, beta):
        if depth == 0 or state.isEnd():
            return self.evaluationFunction(state)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            v = self.getmin(succ, depth, alpha, beta)
            if v >= beta:
                return v
            alpha = max(alpha, v)
            scores.append(v)
        return max(scores)


test = ChessGameState()
agent = AlphaBetaAgent()
print(agent.getAction(test))
