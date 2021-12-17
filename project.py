from model import ChessGameState
import chess


class Agent():
    def getAction(self, state):
        pass


def evalFunction(state, agentColor):
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
        #print('checkmate')
        #print(board.fen)
        return -999999999999 * colors[board.turn == agentColor]
    if board.is_stalemate():
        #print('statemate')
        return 0
    total = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            piece_color = piece.color == agentColor
            piece_symbol = piece.symbol()
            total += colors[piece_color] * values[piece_symbol.lower()]
    return total


class MinimaxAgent(Agent):

    def __init__(self, color, evalFn=evalFunction, depth=2):
        self.evaluationFunction = evalFn
        self.depth = depth
        self.color = color

    def getAction(self, gameState):
        return max(gameState.getLegalActions(),
                   key=lambda x: self.getmin(gameState.generateSuccessor(x), self.depth))

    def getmin(self, state, depth):
        if state.isEnd():
            return self.evaluationFunction(state, self.color)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            scores.append(self.getmax(succ, depth - 1))
        return min(scores)

    def getmax(self, state, depth):
        if depth == 0 or state.isEnd():
            return self.evaluationFunction(state, self.color)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            scores.append(self.getmin(succ, depth))
        return max(scores)


class MinimaxDPAgent(Agent):

    def __init__(self, color, evalFn=evalFunction, depth=2):
        self.evaluationFunction = evalFn
        self.depth = depth
        self.color = color
        self.dp = {}

    def getAction(self, gameState):
        return max(gameState.getLegalActions(),
                   key=lambda x: self.getmin(gameState.generateSuccessor(x), self.depth))

    def getmin(self, state, depth):
        fen = state.getFEN()
        if (fen, depth) not in self.dp:
            if state.isEnd():
                self.dp[fen, depth] = self.evaluationFunction(state, self.color)
            else:
                scores = []
                for x in state.getLegalActions():
                    succ = state.generateSuccessor(x)
                    scores.append(self.getmax(succ, depth - 1))
                self.dp[fen, depth] = min(scores)
        return self.dp[fen, depth]

    def getmax(self, state, depth):
        fen = state.getFEN()
        if (fen, depth) not in self.dp:
            if depth == 0 or state.isEnd():
                self.dp[fen, depth] = self.evaluationFunction(state, self.color)
            else:
                scores = []
                for x in state.getLegalActions():
                    succ = state.generateSuccessor(x)
                    scores.append(self.getmin(succ, depth))
                self.dp[fen, depth] = max(scores)
        return self.dp[fen, depth]


class AlphaBetaAgent(Agent):
    def __init__(self, color, evalFn=evalFunction, depth=2):
        self.evaluationFunction = evalFn
        self.depth = depth
        self.color = color

    def getAction(self, gameState):
        return max(gameState.getLegalActions(),
                   key=lambda x: self.getmin(gameState.generateSuccessor(x), self.depth,
                                             float('-inf'), float('inf')))

    def getmin(self, state, depth, alpha, beta):
        if state.isEnd():
            return self.evaluationFunction(state, self.color)
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
            return self.evaluationFunction(state, self.color)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            v = self.getmin(succ, depth, alpha, beta)
            if v >= beta:
                return v
            alpha = max(alpha, v)
            scores.append(v)
        return max(scores)


class QuiescenceAgent(AlphaBetaAgent):
    def getmax(self, state, depth, alpha, beta):
        if state.isEnd():
            return self.evaluationFunction(state, self.color)
        if depth == 0:
            return self.qmax(state, alpha, beta)
        scores = []
        for x in state.getLegalActions():
            succ = state.generateSuccessor(x)
            v = self.getmin(succ, depth, alpha, beta)
            if v >= beta:
                return v
            alpha = max(alpha, v)
            scores.append(v)
        return max(scores)

    def qmin(self, state, alpha, beta):
        if state.isEnd():
            return self.evaluationFunction(state, self.color)
        scores = []
        for x in filter(state.getBoard().is_capture, state.getLegalActions()):
            succ = state.generateSuccessor(x)
            v = self.qmax(succ, alpha, beta)
            if v <= alpha:
                return v
            beta = min(beta, v)
            scores.append(v)
        return min(scores, default=self.evaluationFunction(state, self.color))

    def qmax(self, state, alpha, beta):
        if state.isEnd():
            return self.evaluationFunction(state, self.color)
        scores = []
        for x in filter(state.getBoard().is_capture, state.getLegalActions()):
            succ = state.generateSuccessor(x)
            v = self.qmin(succ, alpha, beta)
            if v >= beta:
                return v
            alpha = max(alpha, v)
            scores.append(v)
        return max(scores, default=self.evaluationFunction(state, self.color))


#test = ChessGameState()
#agent = QuiescenceAgent(True, depth=2)
#agent2 = AlphaBetaAgent(False, depth=2)
#move1 = agent.getAction(test)
#print(move1)
#test = test.generateSuccessor(move1)
#print(agent2.getAction(test))
