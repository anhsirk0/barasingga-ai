from barasingga import Barasingga
from ai import BarasinggaQlearning

def tuple_board(board):
    return tuple(tuple(row) for row in board)

def train(n):
    player = BarasinggaQlearning()

    for i in range(n):
        print(f"training {i+1}")

        game = Barasingga()

        # Keep track of last move made by either player
        last = {
            1: {"state": None, "action": None},
            2: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = (tuple_board(game.board), game.player)
            action = player.choose_action(state)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = (tuple_board(game.board), game.player)

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            elif game.over:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break
            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player

