from barasingga import Barasingga
import math
import copy
import random

class BarasinggaAI:

    def __init__(self, player=2, depth=4):
        self.player = player
        self.depth = depth
        self.other = Barasingga.other_player(self.player)

    def score(self, board):
        p1 = Barasingga.count_pieces(board, 1)
        p2 = Barasingga.count_pieces(board, 2)
        return p2 - p1

    def terminal(self, board):
        result, winner = Barasingga.game_over(board)
        if result is not None:
            return True
        return False

    def minimax(self, board, maximize=True, depth=4):
        if self.terminal(board) or depth == 0:
            return (None, self.score(board))

        # if maximising player
        if maximize:
            best_score = -math.inf
            all_actions = Barasingga.available_actions(board, self.player)
            best_action = random.choice(all_actions)
            for action in all_actions:
                new = Barasingga.result(board, action)
                score = self.minimax(new, maximize=False, depth=depth - 1)[1]
                if score > best_score:
                    best_score = score
                    best_action = action
            return (best_action, best_score)

        # if not maximising player
        else:
            best_score = math.inf
            all_actions = Barasingga.available_actions(board, self.other)
            best_action = random.choice(all_actions)
            for action in all_actions:
                new = Barasingga.result(board, action)
                score = self.minimax(new, maximize=False, depth=depth - 1)[1]
                if score < best_score:
                    best_score = score
                    best_action = action
            return (best_action, best_score)

    def best_move(self, board):
        depth = self.depth
        temp_board = board.copy()
        return self.minimax(temp_board, depth=depth)[0]


class BarasinggaQlearning:

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of board of 5x5 and player `(board, player)`
         - `action` is a tuple of tuples `((ix, iy), (fx, fy))` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # if q value exist
        if (state, action) in self.q:
            return self.q[(state, action)]
        # else 0
        return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        the_state = (state, action)
        new_value = reward + future_rewards
        # update the q value
        self.q[the_state] = old_q + self.alpha * (new_value - old_q)

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        max_q_value = -math.inf
        tuple_board, player = state
        board = self.list_board(tuple_board)
        actions = Barasingga.available_actions(board, player)
        if len(actions) == 0:
            return 0

        for action in actions:
            the_state = (state, action)

            if the_state in self.q:
                q_value = self.q[the_state]
            else:
                q_value = 0

            if q_value > max_q_value:
                max_q_value = q_value

        return max_q_value

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        q_value = -math.inf
        tuple_board, player = state
        board = self.list_board(tuple_board)
        actions = Barasingga.available_actions(board, player)
        best_action = random.choice(actions)
        for action in actions:
            the_state = (state, action)
            if the_state  in self.q and self.q[the_state] >= q_value:
                best_action = action
                q_value = self.q[the_state]

        if epsilon:
            if len(actions) > 1:
                actions.remove(best_action)
                total = [best_action] * 9 * len(actions) + list(actions) 
                return random.choice(total)
        return best_action

    def list_board(self, board):
        return [list(row) for row in board]

