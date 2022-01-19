# not_chess
This is not a multiplayer terminal based chess application

## Functionality
- Fully functional chess played through the command line
- Http based multiplayer

## What is missing
- Single player/no server
- Closing games
- Seeing a list of current games
- Timers (probably never going to be added)
- any form of security to stop cheating, this was made to play with people that you know!
- a way to message your opponent

## How to play 
Currently everything is run from python and so requres python to be instlled on your system

### Server
#### Manual
1. Mmake sure chess and flask are installed
    ```
    pip install chess
    pip install flask
    ```
2. Make sure port 5000 is exposed, optionally you can change the port to whatever you want by modifying server.py
3. Run server.py
    ```
    python <dir_to_server.py>
    ```
#### Docker
optionally you can also host a server by running the docker container
this can be built using the docker file provided or can obtained from docker hub (WARNING THE DOCKER HUB IMAGE MIGHT BE OUTDATED)
https://hub.docker.com/r/blacklion11/notchess
Make sure the port you choose (default 5000) is exposed
### Client
1. Run client,py
    ```
    python <dir_to_client.py>
    ```
    
### Client commands
- not in a game
  - create
    - Used to create a game, will be promted to give the game a name. this name will be used by your opponent to join
  - join 
    - used to join a game, will be promted to provide a name. If you close your terminal mid game you can reconnect by using the same username and the join command
- In a game
  - board
    - returns the games board
  - pga
    - returns the pga of the current game
  - fen
    - returns the fen representation of the current board
  - moves
    - returns a list of the moves made so far
  - legal_moves
    - returns the legal moves the current player can make
  - MOVE
    - not a command but represents a move you want to make eg (e5,Qxb3,0-0 Etc) 
