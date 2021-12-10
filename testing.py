import chess
from model import ChessGameState
from project import MinimaxAgent, AlphaBetaAgent, QuiescenceAgent

agent = AlphaBetaAgent(True, depth=3)
agent2 = MinimaxAgent(False, depth=2)
game = ChessGameState()
turn = True

while not game.isEnd():
    agents = {True: agent, False: agent2}
    move = agents[turn].getAction(game)
    print(turn, move)
    game = game.generateSuccessor(move)
    print(game.getBoard())
    turn = not turn

print(not game.getTurn())