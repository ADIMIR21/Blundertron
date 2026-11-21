import chess.pgn
import chess.engine
from io import StringIO
import math

engine = chess.engine.SimpleEngine.popen_uci(
    "engines\ember.exe" 
)
pgn = '''none'''

def read_png (png_text):
    return chess.pgn.read_game(StringIO(png_text))

def winning(board, color):
    info = engine.analyse(
    board,
    chess.engine.Limit(time=2.0)
    )
    if not info["score"].is_mate(): 
        score = info["score"].pov(color).score(mate_score=100000) 
        win = 50 + 50 * (2 / (1 +  math.exp(-0.00368208 * score)) - 1)
    else:
        win = info["score"].pov(color).mate()
    return win, info["score"].is_mate()

def processing(win, win_old, mat_old, mat):
    if not mat and not mat_old:
        loss = win_old - win
        Accuracy = 100
        if loss > 0:
            Accuracy = 103.1668 * math.exp(-0.04354 * loss) - 3.1669
        return loss, Accuracy
    if not mat_old and mat:
        return win, None
    if mat_old and mat:
        return win, None
    if mat_old and not mat:
        return win, None

def estimation(comparisons):
    if comparisons <= 10:
        return "best"
    if comparisons <= 30:
        return "good"
    if comparisons <= 70:
        return "inaccuracy"
    if comparisons <= 150:
        return "error"
    else:
        return "yawn" 

game = read_png(pgn)
board = game.board()
i = 0.5

for move in game.mainline_moves():
    win_old, mat_old = winning(board, board.turn)
    board.push(move)
    i += 0.5 
    win, mat = winning(board, not board.turn)
    result_Accuracy = None 
    result_loss, result_Accuracy  = processing(win, win_old, mat_old, mat)
    color =  "white" if not board.turn else "black"
    if result_Accuracy == None:
       print(f"move:{i} checkmate against the player in {abs(result_loss)} moves, color:{color}") if result_loss < 0 else print(f"move:{i} checkmate in favor of the player in {result_loss} moves, color:{color}")
    else:
        print(f"move:{i} loss or gain:{result_loss} accuracy:{result_Accuracy} color:{color}")
print("game over")
engine.quit()