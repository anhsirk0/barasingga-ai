# Barasingga and AI

## Barasingga is a simple two-player folk-game

## Rules:
 - 12 pieces for each player
 - any piece can move one step only to any of its connected neighbor
 - captures are made only by hoping over opponent's piece (over one piece only)
 - one move is allowed to move at each turn
 - two or more consecutive captures is possible if one only with the same piece (see fig 5)
  -- this rule is yet to be implemented
## Initial position
![screenshot2.png](https://github.com/anhsirk0/barasingga-ai/blob/master/assets/screenshot2.png)

## moves
![moves.png](https://github.com/anhsirk0/barasingga-ai/blob/master/assets/moves.png)


## Captures
> vertical capture
![capture.png](https://github.com/anhsirk0/barasingga-ai/blob/master/assets/capture.png)

> diagonal capture
![diagonal_capture.png](https://github.com/anhsirk0/barasingga-ai/blob/master/assets/diagonal_capture.png)

> two captures in one turn
> red piece at (1, 3) can capture two pieces (1, 2) & (2, 1) and its final position will be (3, 1)
> similarly for blue piece at (4, 2) it can capture (3, 2) & (2, 3) and its final position willbe (2, 5)
![two_captures.png](https://github.com/anhsirk0/barasingga-ai/blob/master/assets/two_captures.png)

# AI
## minimax and Q-learning algorithm is implemented

### algorithm overview
## Minimax
A minimax algorithm is a recursive algorithm for choosing the next move in an n-player game, usually a two-player game.
A value is associated with each position or state of the game.
This value is computed by means of a position evaluation function and it indicates how good it would be for a player to reach that position.
Sources:
https://en.wikipedia.org/wiki/Minimax
https://www.youtube.com/watch?v=l-hh51ncgDI

## Q-learning

Q-learning is a model-free reinforcement learning algorithm to learn the value of an action in a particular state.
It does not require a model of the environment (hence "model-free"), and it can handle problems with stochastic transitions and rewards without requiring adaptations."")


### insights (for this specific problem)
minimax performs better than a model trained by q-learning
q-learning is not suitable for two agents
minimax with depth 5 is not as good as human

minimax (depth 4) was able to beat the Q-learn model trained on 5000 games

## file structure
barasingga.py - main file that holds class for Barasingga game
ai.py - Minimax and Q-learning AI are implemented in this file
play.py - To train the Q-learn model
runner.py - pygame gui to play/view (usage: click a piece to choose click again to an empty location to move/capture)
