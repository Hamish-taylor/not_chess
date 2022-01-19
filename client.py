import requests
import json
import time
import os
from threading import Thread
import sys


white = None
stop_threads = False
user_name = ""
game_name = ""

def main():
    global user_name
    global game_name
    global stop_threads
    global white
    try:
        server_address = None
        #connect to server
        while user_name == "":
            user_name = input("Enter your username: ")


        while server_address == None:
            server_address = input("Server address:")

            response = None
            try:
                response = requests.get(f"http://{server_address}/health")
                print("Server is up")
            except requests.exceptions.RequestException as e:
                print("Server is down")
                server_address = None

        #create or join game
        not_in_game = True
        while not_in_game:
            inp = input()
            if "create" in inp:
                game_name = input("Enter game name: ")
                response = requests.post(f"http://{server_address}/create_game", json={"game_name": game_name, "user_name": user_name})

                print(response.text)
                not_in_game = False
            elif "join" in inp:
                game_name = input("Game name:")
                response = requests.post(f"http://{server_address}/join_game", json={"game_name": game_name, "user_name": user_name})
                print(response.text)
                white = response.json()["white"]
                not_in_game = False
        t = Thread(target=check_turn,args=(server_address,))

        t.start()

        while True:
            time.sleep(1)
            inp = input()
            if "exit" in inp:
                raise KeyboardInterrupt()

            request = {"move" : str(inp), "game_name": game_name, "user_name": user_name}
            response = requests.post(f"http://{server_address}/move", json=request, allow_redirects=True,headers={"Content-Type": "application/json"})
            print(json.loads(response.text)["response"])
    except KeyboardInterrupt:
        print("\nExiting...")
        stop_threads = True
        sys.exit()

def check_turn(server_address):
    global stop_threads
    global white
    turn = "white"
    old_turn = "old"
    turn = requests.get(f"http://{server_address}/turn")
    while True:
        time.sleep(1)
        resp = requests.get(f"http://{server_address}/turn", json={"game_name": game_name, "user_name": user_name})

        if "turn" not in resp.text:
            print(resp.text)
        else:
            turn = resp.json()["turn"]

            if white == None:
                white = resp.json()["white"]

            if(turn != old_turn):
                os.system('cls' if os.name == 'nt' else 'clear')
                if resp.json()["moves"] != []:
                    t = "Black" if len(resp.json()["moves"])%2 == 0 else "White"
                    print(t + " moved " + resp.json()["moves"][len(resp.json()["moves"])-1])
                
                old_turn = turn
                
                print("It is " + turn + "'s turn - you are " + ("white" if white else "black"))
        if(stop_threads):
            break
            
        
if __name__ == "__main__":
    main()