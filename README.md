# Minimax Algorithm
The checkers game code has been modified to simulate a game where each AI player decides its next move using the minimax algorithm with alpha-beta pruning.

## How to Run
Navigate to the src directory and run the following command:
```
$ python main.py
```

## Parameters
You can set the minimax algorithm's depth for each player in ```src/main.py```. You can change ```WHITE_DEPTH``` and ```RED_DEPTH``` parameters to your desired value. Note that the algorithm is too slow for depths higher than 5.