import chess
from model import ChessGameState
from project import MinimaxAgent, AlphaBetaAgent, QuiescenceAgent
import time

agent = MinimaxAgent(True, depth=3)
agent2 = MinimaxAgent(False, depth=2)
game = ChessGameState()
turn = True
agents = {True: agent, False: agent2}

agent.getAction(game)
print(game.getCount())

# total = 0
# for x in range(1, 101):
#     print(x)
#     start = time.time()
#     agent.getAction(game)
#     cur = time.time() - start
#     file = open('quiescence.txt', 'a')
#     file.write('%f\n' % cur)
#     file.close()
#     print(cur)
#     total += cur
#     print(total / x)

# while not game.isEnd():
#     move = agents[turn].getAction(game)
#     print(turn, move)
#     game = game.generateSuccessor(move)
#     print(game.getBoard())
#     turn = not turn

# print(not game.getTurn())