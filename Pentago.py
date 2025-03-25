"""
Author: Andrew Walsh
GitHub username: walshrandrew
Date: 7/29/2024
Description: A two player strategy game called Pentago.
            players take turns placing a marble of choice onto an unoccupied space on the 6x6 board.
            After placing a marble, the player then rotates 90 degrees any one of the sub-boards either clockwise
            or counterclockwise.
            Win condition: A player wins by getting five of their marbles in a vertical, horizontal, or diagonal row.
            Draw condition: all spaces are occupied without forming a row of five after the rotation.
                            or both players achieve five in a row AFTER the rotation simultaneously.
"""


class Pentago:
    """
    One class to rule them all.
    Holds all methods so that you can initialize the game by calling the class Pentago.
    Handles all game conditions, win conditions, board conditions, and moves for both players.
    """

    def __init__(self):
        self._game_board = [['[ ]' for _ in range(6)] for _ in range(6)]
        self._game_state = 'UNFINISHED'
        self._current_player = ' B '

    def get_game_state(self):
        """ returns current game state """
        return self._game_state

    def get_game_board(self):
        """ returns the current game board """
        return self._game_board

    def get_current_player(self):
        """ returns teh current player """
        return self._current_player

    def set_game_state(self, state):
        """ sets the current game state """
        self._game_state = state

    def set_current_player(self, player):
        """ sets the current player """
        self._current_player = player

    def is_board_full(self):
        """
        Iterates through the board to check if any space is empty
        :return: False if empty cell found; True if no empty cells found
        """
        for row in self._game_board:
            for cell in row:
                if cell == '[ ]':
                    return False  # Empty cell found
        return True  # No empty cells found

    def win_condition(self, color):
        '''
        checks if a player has achieved a 5 in a row
        calls method before and after the rotation to determine the win state
        :return: True if player won, and False if no win condition met yet
        '''
        for row in range(6):
            for col in range(6):
                if self._five_in_row(color, row, col):
                    return True
        return False

    def _five_in_row(self, color, row, col):
        '''
        Checks for 5 in a row for horizontal, vertical, and diagonal lines
        '''
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # right, down, down-right diagonal, down-left diagonal
        for board_row, board_column in directions:
            count = 0

            # Check positive direction
            for i in range(-4, 1):
                r = row + i * board_row
                c = col + i * board_column
                if 0 <= r < 6 and 0 <= c < 6 and self.get_game_board()[r][c] == color:
                    count += 1
                else:
                    count = 0
                if count == 5:
                    return True

            # Check negative direction
            count = 0
            for i in range(1, 5):
                r = row - i * board_row
                c = col - i * board_column
                if 0 <= r < 6 and 0 <= c < 6 and self.get_game_board()[r][c] == color:
                    count += 1
                else:
                    break
                if count == 5:
                    return True
        return False

    def rotate_sub_board(self, sub_board, rotation):
        '''
        Rotates the sub_board given the sub_board number and the rotation direction
        Uses a dictionary sub_boards to correspond to 3x3 sub_boards
        Uses slice objects and cuts the board into 4 sub_boards
        Extract sub_board into 3 matrix so you can rotate them
        Rotate sub_board with the matrix
        Re implement the extracted sub_board back onto the main board.
        '''
        sub_boards = {
            1: (slice(0, 3), slice(0, 3)),
            2: (slice(0, 3), slice(3, 6)),
            3: (slice(3, 6), slice(0, 3)),
            4: (slice(3, 6), slice(3, 6))
        }

        row_slice, col_slice = sub_boards[sub_board]
        sub_board_matrix = [row[col_slice] for row in self.get_game_board()[row_slice]]
        rotated_matrix = self.rotate_board_section(sub_board_matrix, rotation)

        for i in range(3):
            self.get_game_board()[row_slice.start + i][col_slice.start:col_slice.start + 3] = rotated_matrix[i]

    @staticmethod
    def rotate_board_section(section, rotation):
        '''
        A static method for: Rotates the 3x3 section 90 degrees clockwise and/or anticlockwise
        Rotates clockwise with 'C'
        Rotates anticlockwise with 'A'
        :return: rotate
        '''
        rotate = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if rotation == 'C':
                    rotate[j][2 - i] = section[i][j]
                elif rotation == 'A':
                    rotate[2 - j][i] = section[i][j]
        return rotate

    def make_move(self, color, position, sub_board, rotation):
        """
        Handles a player's move by placing a marble, rotating a sub_board, and updating the game_state.

        The method:
        - Validates the move (game is unfinished, correct player's turn, empty position)
        - Places the marble on the board.
        - Checks for win conditions before and after rotating the chosen sub_board.
        - Updates the game state (unfinished, winner, or draw) and switches turns if the game is unfinished.

        :param color: ' W ' or ' B ', White or Black marbles
        :param position: The position to place the marble (ie., a1, b5, etc.)
        :param sub_board: an integer of either 1, 2, 3 or 4 that represents the sub-board the player choose to rotate
        :param rotation: a string that represent the direction the sub-board will rotate, either ‘C’ (clockwise) or ‘A’ (anti-clockwise).
        :return: A message if move is invalid, game is finished, not this player's turn, or Position is not empty
        :return: True if move was successfully made.
        """
        row, col = ord(position[0]) - ord('a'), int(position[1])

        # validate the move
        if self.get_game_state() != 'UNFINISHED':     # Check if the game is already finished
            return 'Game is finished'
        if color != self.get_current_player():        # Ensure the correct player is making the move
            return "Not this player's turn"
        if self.get_game_board()[row][col] != '[ ]':  # Ensure the chosen position is empty
            return 'Position is not empty'

        # Place marble on board
        self.get_game_board()[row][col] = color

        # Check for winning condition using win_condition method
        if self.win_condition(color):
            self.set_game_state(f'{color} wins')
            self.set_current_player(' W ' if color == ' B ' else ' B ')  # Update player's turn
            return True

        # Rotate the chosen sub_board using rotate_sub_board method
        self.rotate_sub_board(sub_board, rotation)

        # Check for winning condition again using win_condition method
        black_wins = self.win_condition(' B ')
        white_wins = self.win_condition(' W ')

        # If black and white win AFTER rotation then 'DRAW'
        if black_wins and white_wins:
            self.set_game_state('DRAW')
        elif black_wins:
            self.set_game_state('Black wins')
        elif white_wins:
            self.set_game_state('White wins')

        # If no winner but board is full, then 'DRAW'
        elif self.is_board_full():
            if not (self.win_condition(' B ') or self.win_condition(' W ')):
                self.set_game_state('DRAW')
            else:
                self.set_game_state('UNFINISHED')

        # Update the game state and player's turn.
        if self.get_game_state() == 'UNFINISHED':
            self.set_current_player(' W ' if color == ' B ' else ' B ')

        return True

    def print_board(self):
        """
        outputs the current state of the board.
        :return: a 2D picture of the board.
            0   1   2   3   4   5
        a  [ ] [ ] [ ] [ ] [ ] [ ]
        b  [ ] [ ] [ ] [ ] [ ] [ ]
        c  [ ] [ ] [ ] [ ] [ ] [ ]
        d  [ ] [ ] [ ] [ ] [ ] [ ]
        e  [ ] [ ] [ ] [ ] [ ] [ ]
        f  [ ] [ ] [ ] [ ] [ ] [ ]
        """
        print('   0 ', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ')
        for bcdef, row in enumerate(self.get_game_board()):
            print(chr(ord('a') + bcdef), ' '.join(row))


print("test1  # Expected output: Basic moves and rotation and check winning condition")
game = Pentago()
print(game.make_move(' B ', 'a2', 1, 'C'))  # Place black marble at a2, rotate sub_board 1 clockwise
print(game.make_move(' W ', 'a2', 1, 'C'))  # Place white marble at a2, rotate sub_board 1 clockwise
print(game.is_board_full())                                                # False
game.print_board()
print(game.get_game_state())                                               # UNFINISHED
print('\n')


print("test2 # Expected output: Invalid moves")
game = Pentago()
print(game.make_move(' B ', 'a0', 1, 'C'))  # Place black marble at a0, rotate sub_board 1 clockwise
game.rotate_sub_board(1, 'a')                             # Rotate sub-board 1 anticlockwise (reset sub_board1)
print(game.make_move(' W ', 'a0', 1, 'C'))  # Place white marble at a0, Invalid, position is not empty
print(game.make_move(' B ', 'b0', 1, 'C'))  # Not player's turn (should be W's)
print(game.make_move(' B ', 'c0', 1, 'C'))  # Not player's turn (should still be W's
print(game.make_move(' W ', 'a0', 1, 'C'))  # Check if sub_board rotates on invalid input. Invalid, position is not empty.
print('\n')

print("test3  # Expected output: Rotate all sub boards and check board state")
game = Pentago()
print(game.make_move(' B ', 'a0', 1, 'C'))  # Place black marble at a0, rotate sub_board 1 clockwise
print(game.make_move(' W ', 'a3', 2, 'C'))  # Place white marble at a3, rotate sub_board 2 clockwise
print(game.make_move(' B ', 'd2', 3, 'C'))  # Place black marble at d2, rotate sub_board 3 clockwise
print(game.make_move(' W ', 'd3', 4, 'C'))  # Place white marble at d3, rotate sub_board 4 clockwise
game.print_board()
print('\n')


print("test4  # Expected output: Diagonal win for ' W ' white")
game = Pentago()
moves = [
    (' B ', 'a0', 1, 'C'), (' W ', 'a1', 1, 'C'), (' B ', 'a2', 1, 'C'),
    (' W ', 'a3', 1, 'C'), (' B ', 'a4', 1, 'C'), (' W ', 'b0', 3, 'A'),
    (' B ', 'b1', 3, 'A'), (' W ', 'b2', 3, 'A'), (' B ', 'b3', 3, 'A'),
    (' W ', 'b4', 3, 'A'), (' B ', 'c0', 2, 'C'), (' W ', 'c1', 2, 'C'),
    (' B ', 'c2', 2, 'C'), (' W ', 'c3', 2, 'C'), (' B ', 'c4', 2, 'C'),
    (' W ', 'd0', 4, 'A'), (' B ', 'd1', 4, 'A'), (' W ', 'd2', 4, 'A'),
    (' B ', 'd3', 4, 'A'), (' W ', 'd4', 4, 'A'), (' B ', 'e0', 1, 'C'),
    (' W ', 'e1', 1, 'C'), (' B ', 'e2', 1, 'C'), (' W ', 'e3', 1, 'C'),
    (' B ', 'e4', 1, 'C'), (' W ', 'f0', 2, 'A'), (' B ', 'f1', 2, 'A'),
    (' W ', 'f2', 2, 'A'), (' B ', 'f3', 2, 'A'), (' W ', 'f4', 2, 'A')
]
for move in moves:
    game.make_move(*move)
print(game.is_board_full())  # Expected: False
print(game.get_game_state())  # Expected: white won
game.print_board()
print('\n')


print("test5  # Expected output: Make sure a player can not go more than once per turn")
game = Pentago()
game.make_move(' B ', 'a0', 1, 'C')  # Places black marble
game.make_move(' B ', 'a1', 1, 'C')  # Invalid, white's turn
game.make_move(' W ', 'c2', 1, 'C')  # Invalid, white's turn
game.print_board()
print('\n')

print("test6  # Expected output: Draw")
game = Pentago()
moves = [
        (' B ', 'a0', 4, 'C'), (' W ', 'a1', 4, 'C'), (' B ', 'a2', 4, 'C'),
        (' W ', 'b0', 4, 'C'), (' B ', 'b1', 4, 'C'), (' W ', 'b2', 4, 'C'),
        (' B ', 'c0', 4, 'C'), (' W ', 'c1', 4, 'C'), (' B ', 'c2', 4, 'C'),
        (' W ', 'a3', 4, 'C'), (' B ', 'a4', 4, 'C'), (' W ', 'a5', 4, 'C'),
        (' B ', 'b3', 4, 'C'), (' W ', 'b4', 4, 'C'), (' B ', 'b5', 4, 'C'),
        (' W ', 'c4', 4, 'C'), (' B ', 'c3', 4, 'C'), (' W ', 'c5', 4, 'C'),
        (' B ', 'd0', 4, 'C'), (' W ', 'e0', 4, 'C'), (' B ', 'f0', 4, 'C'),
        (' W ', 'd3', 3, 'C'), (' B ', 'e3', 3, 'C'), (' W ', 'f3', 3, 'C'),
        (' B ', 'd0', 4, 'C'), (' W ', 'd1', 4, 'C'), (' B ', 'd3', 4, 'C'),
        (' W ', 'd4', 3, 'C'), (' B ', 'd1', 4, 'C'), (' W ', 'e1', 1, 'C'),
        (' B ', 'f1', 1, 'C'), (' W ', 'f2', 1, 'A'), (' B ', 'd4', 1, 'C'),
        (' W ', 'e4', 1, 'C'), (' B ', 'd5', 1, 'A'), (' W ', 'f4', 1, 'C'),
    ]
for move in moves:
    game.make_move(*move)
print(game.is_board_full())  # Expected: True
print(game.get_game_state())  # Expected: 'DRAW'
game.print_board()
print('\n')