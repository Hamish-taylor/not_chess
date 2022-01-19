from flask import Flask, request, jsonify
from random import randint
import chess
import chess.pgn
board = chess.Board()
white = True
finished = False

games = {}

from werkzeug.exceptions import BadRequest



aip_http_port = "5000"

app = Flask(__name__)


@app.route("/health")
def handle_health():
    return "I'm healthy!\n"

@app.route("/turn")
def handle_turn():
    req = request.get_json(force=True)
    resp = ""

    if "game_name" not in req or "user_name" not in req:
        raise BadRequest(description="game_name/username missing")
    else:
        game_name = req["game_name"]
        if len(games[game_name]["players"]) < 2:
            return "Waiting for opponent"
        else:
            return {"turn" : "white" if games[str(req["game_name"])]["white"] else "black", "white" : games[str(req["game_name"])][req["user_name"]], "moves" : games[str(req["game_name"])]["moves"]}

@app.route(
    "/create_game",
    methods=["POST"],
)
def create_game():
    global games
    req = request.get_json(force=True)
    
    
    if "game_name" in req and "user_name" in req:
        game_name = req["game_name"]
        user_name = req["user_name"]
        if game_name == "" or user_name == "":
            raise BadRequest(description="username/gamename is empty")
        games[str(game_name)] = {'board':chess.Board(), 'players':[user_name], 'white':True, 'moves':[]}
    else :
        raise BadRequest(description="username not found")

    response = {"response": "game created successfully"}

    return jsonify(response), 200, {"Content-Type": "application/json; charset=utf-8"}

@app.route(
    "/join_game",
    methods=["POST"],
)
def join_game():
    
    req = request.get_json(force=True)
    
    if "game_name" in req and "user_name" in req:
        game_name = req["game_name"]
        user_name = req["user_name"]
        if game_name == "" or user_name == "":
            raise BadRequest(description="username/gamename is empty")
        if game_name in games:
            if len(games[game_name]['players']) == 1:
                games[game_name]['players'].append(user_name)
            elif user_name in games[game_name]['players']:
                response = {"response": "game rejoined successfully" , "white": games[game_name][user_name]}
                return jsonify(response), 200, {"Content-Type": "application/json; charset=utf-8"}
            else:
                raise BadRequest(description="game is full")
    else :
        raise BadRequest(description="username/game not found")

    #assign teams
    
    

    white = randint(0,1)


    games[str(req["game_name"])][req["user_name"]] = True if white == 0 else False

    black = games[str(req["game_name"])]["players"][0] 
    games[str(req["game_name"])][black] = False if white == 0 else True

    response = {"response": "game join successfully" , "white": True if white == 0 else False}

    return jsonify(response), 200, {"Content-Type": "application/json; charset=utf-8"}
@app.route(
    "/move",
    methods=["POST"],
)
def handle_move():
    
    req = request.get_json(force=True)
    
    (move,user_name,game_name) = validate_request(req)
    print(move)

    if(len(games[game_name]["players"]) == 1):
        raise BadRequest(description="you have no opponent!")

    response = {"ERROR": "wow"}

    global white
    global finished
    if not finished:
        resp = process_input(move,game_name)
        response = {"response": str(resp)}
    return jsonify(response), 200, {"Content-Type": "application/json; charset=utf-8"}

@app.route(
    "/moves",
    methods=["GET"],
)
def valid_moves():
    global white
    turn = "white" if white else "black"

    response = {str(turn) : str(board.legal_moves)}

    return jsonify(response), 200, {"Content-Type": "application/json; charset=utf-8"}



def validate_request(req):

    if "user_name" in req and "game_name" in req and games[req["game_name"]]["white"] == games[req["game_name"]][req["user_name"]]:
        return (req["move"],req["user_name"],req["game_name"])
    elif "moves" in req["move"] or "fen" in req["move"] or "board" in req["move"] or "legal_moves" in req["move"] or "pgn" in req["move"]:
        return (req["move"],req["user_name"],req["game_name"])
    else:
        raise BadRequest(description="Its not your turn")



@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = {
        "response": e.description
    }
    return jsonify(response), 400, {"Content-Type": "application/json; charset=utf-8"}



def process_input(input,game_name):
    out = ""
    global white
    board = games[game_name]['board']
    if input == "board":
        return board
    elif input == "legal_moves":
        return board.legal_moves
    elif input == "moves":
        return games[game_name]["moves"]
    elif input == "fen":
        return board.fen()
    elif input == "pgn":
        return chess.pgn.Game.from_board(board)
    else:
        try:
            board.push_san(input)
            games[game_name]["moves"].append(input)
            games[game_name]["white"] = not games[game_name]["white"]
        except Exception as e:
            raise BadRequest(description="invalid move")
        
    out += check_check()
    out += check_stalemate()
    out += check_checkmate()
    out += check_insufficient_material()
    out += check_fivefold_repetition()
    return out
    


def check_check():
    if(board.is_check()):
        if(white):
            return "White is in check\n"
        else:
            return "Black is in check\n"
    return ""

def check_stalemate():
    global finished
    if(board.is_stalemate()):
        finished = True
        return "Game has finished in Stalemate\n"
    return ""

def check_checkmate():
    global finished
    if(board.is_checkmate()):
        finished = True
        if(white):
            return ("Black wins\n")
        else:
            return ("White wins\n")
    return ""   

def check_insufficient_material():
    global finished
    if(board.is_insufficient_material()):
        finished = True
        return("Game has finished in Insufficient Material\n")
    return ""    

def check_fivefold_repetition():
    global finished
    if(board.is_fivefold_repetition()):
        finished = True
        return("Game has finished in Fivefold Repetition\n")
    return ""    

if __name__ == "__main__":
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.run(host="0.0.0.0", port=aip_http_port)


