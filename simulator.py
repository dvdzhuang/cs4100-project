import project
import model
import chess

board = model.ChessGameState(board=chess.Board(fen=input()))
agent = project.AlphaBetaAgent(depth=2)
print(agent.getAction(board))
print(board.getBoard())