import copy

class Barasingga:

    def __init__(self):
        """
        Initialize game board
        """
        self.board = self.create_board()
        self.player = 1
        self.winner = None
        self.draw = False
        self.over = False
        self.turn = False

    def create_board(self):
        board = [[1]*5 for i in [1, 2]]
        board += [[1, 1, 0, 2, 2]]
        board += [[2]*5 for i in [1, 2]]
        return board

    def print_board(self):
        separator = "--"
        for i in range(5):
            row = self.board[i]
            s = f" [{row[0]}]--[{row[1]}]--[{row[2]}]--[{row[3]}]--[{row[4]}]"
            print(s)
        print()

    @classmethod
    def count_pieces(cls, board, player):
        return sum([row.count(player) for row in board])

    @classmethod
    def get_moves(cls, point, board, player):
        """
        Possible moves and captures for a given point in all directions
        captures:                           moves:
        [ ]         [ ]         [ ]
            \        |        /
              [2]   [2]   [2]              [ ]   [ ]   [ ]
                  \  |  /                      \  |  /
        [ ]-- [2] -- 1 -- [2] --[ ]        [ ] -- 1 -- [ ]
                  /  |  \                      /  |  \
              [2]   [2]   [2]              [ ]   [ ]   [ ]
            /        |        \
        [ ]         [ ]         [ ]
        """
        y, x = point
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # final points
                fy = y + i
                fx = x + j
                no_negative_indexes = min(fy, fx) >= 0
                if (i == 0 or j == 0) and i != j and no_negative_indexes:
                    try:
                        # check if the position is empty
                        if board[y + i][x + j] == 0:
                            moves.append((y + i, x + j))
                    except IndexError:
                        continue

        captures = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # final points
                fy = y + 2 * i
                fx = x + 2 * j
                # middle points
                my = y + 1 * i
                mx = x + 1 * j
                no_negative_indexes = min(fy, fx, my, mx) >= 0
                if (i == 0 or j == 0) and i != j and no_negative_indexes:
                    try:
                        # final position should be empty
                        final = board[y + 2 * i][x + 2 * j]
                        # middle position should be other_player's piece
                        middle = board[y + i][x + j]
                        if final == 0 and middle not in [0, player]:
                            captures.append((y + 2 * i, x + 2 * j))
                    except IndexError:
                        continue

        # diagonal moves and captures
        neighbors = {}
        neighbors[(0, 2)] = ["downright", "downleft"]
        neighbors[(1, 1)] = ["upright", "downleft"]
        neighbors[(1, 3)] = ["downright", "upleft"]
        neighbors[(2, 0)] = ["downright", "upright"]
        neighbors[(2, 4)] = ["upleft", "downleft"]
        neighbors[(3, 1)] = ["upleft", "downright"]
        neighbors[(3, 3)] = ["upright", "downleft"]
        neighbors[(4, 2)] = ["upleft", "upright"]

        if point in neighbors:
            directions = neighbors[point]
            for direction in directions:
                if direction == "upleft":
                    m = (y - 1, x - 1)
                    c = (y - 2, x - 2)
                elif direction == "upright":
                    m = (y - 1, x + 1)
                    c = (y - 2, x + 2)
                elif direction == "downleft":
                    m = (y + 1, x - 1)
                    c = (y + 2, x - 2)
                else:
                    m = (y + 1, x + 1)
                    c = (y + 2, x + 2)

                # check validity of move
                try:
                    m_piece = board[m[0]][m[1]]
                    if m_piece == 0:
                        moves.append(m)
                except IndexError:
                    m_piece = 0
                    continue

                # check validity of capture
                try:
                    c_piece = board[c[0]][c[1]]
                    if c_piece == 0 and m_piece not in [0, player]:
                        captures.append(c)
                except IndexError:
                    continue
        return moves + captures

    @classmethod
    def available_actions(cls, board, player):
        """
        All valid actions for a given player and a board
        """
        actions = []
        for x in range(5):
            for y in range(5):
                if board[y][x] == player:
                    moves = Barasingga.get_moves((y, x), board, player)
                    for move in moves:
                        actions.append(((y, x), move))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Return the player that is not `player`.
        """
        return 2 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Barasingga.other_player(self.player)

    @classmethod
    def result(cls, board, action):
        """
        Return the resulting board after taking an action on a board
        `action` as ((initial position), (final position))
        """
        initial, final = action
        iy, ix = initial
        fy, fx = final

        result_board = copy.deepcopy(board)

        # detect a capture
        dx = abs(fx - ix)
        dy = abs(fy - iy)
        if max(dx, dy) == 2:
            # remove captured piece
            # diagonal capture
            if dx == dy:
                result_board[int(fy / 2 + iy / 2)][int(fx / 2 + ix / 2)] = 0
            # horizontal capture
            elif dx == 2:
                result_board[fy][int(fx/2 + ix/2)] = 0
            # vertical capture
            elif dy == 2:
                result_board[int(fy/2 + iy/2)][fx] = 0

        # make move
        result_board[fy][fx] = board[iy][ix]
        result_board[iy][ix] = 0

        return result_board

    def move(self, action):
        """
        Make a move on game
        """
        result_board = self.result(self.board, action)
        self.board = result_board.copy()
        # check for errors
        if self.winner is not None:
            raise Exception("Game already won")

        # check for game over
        result, winner = self.game_over(self.board)
        if winner is not None:
            self.winner = winner

        if result is not None:
            self.over = True
            if result == "draw":
                self.draw = True

        self.switch_player()
        self.print_board()

    @classmethod
    def game_over(cls, board):
        p1_pieces = cls.count_pieces(board, 1)
        p2_pieces = cls.count_pieces(board, 2)

        winner = None
        result = None

        if p1_pieces in [1, 2] and p2_pieces in [1, 2]:
            result = "draw"

        elif p1_pieces == 0:
            result = "over"
            winner = 2

        elif p2_pieces == 0:
            result = "over"
            winner = 1

        return (result, winner)
