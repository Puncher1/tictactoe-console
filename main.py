from copy import deepcopy
import os
import sys
import random
import time


class TicTacToe:

    def __init__(self):
        self.grid = [[" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]]

        self.invalid_input = False
        self.field_already_used = False

    def get_possible_fields(self, grid):
        possible_fields = []
        for i, row in enumerate(grid):
            for j, field in enumerate(row):
                if field == " ":
                    possible_fields.append((i, j))
        return possible_fields

    def get_coordinates(self, field):
        letter = field[0]
        num = field[1]

        letter_dict = {
            "A": 0,
            "B": 1,
            "C": 2,
        }
        coordinates = (int(num) - 1, letter_dict[letter])

        return coordinates

    def get_random_coordinates(self, possible_fields):
        rand_field = random.choice(possible_fields)
        return rand_field[0], rand_field[1]

    def get_termination_state(self, grid):
        if self.check_winner("X", grid):
            return 10
        elif self.check_winner("O", grid):
            return -10

    def check_field(self, field):
        if field != " ":
            self.field_already_used = True

    def check_input(self, input_str):
        if not len(input_str) == 2:
            self.invalid_input = True
            return

        letter = input_str[0]
        num = input_str[1]

        if letter not in ["A", "B", "C"] or num not in ["1", "2", "3"]:
            self.invalid_input = True

    def check_winner(self, player, grid):
        # horizontal check
        for i in range(3):
            count_h = 0
            for j in range(3):
                field = grid[i][j]
                if field == player:
                    count_h += 1

            if count_h == 3:
                return True

        # vertical check
        for i in range(3):
            count_v = 0
            for j in range(3):
                field = grid[j][i]
                if field == player:
                    count_v += 1

            if count_v == 3:
                return True

        # diagonal check
        count_d = 0
        for i in range(3):
            field = grid[i][i]
            if field == player:
                count_d += 1

        if count_d == 3:
            return True

        d = 2
        count_d = 0
        for i in range(3):
            field = grid[d][i]
            if field == player:
                count_d += 1

            d -= 1

        if count_d == 3:
            return True

        return False

    def minimax(self, temp_grid, is_maximizer):
        possible_fields = self.get_possible_fields(temp_grid)
        state = self.get_termination_state(temp_grid)

        if state == 10:
            return state
        elif state == -10:
            return state

        if not possible_fields:
            return 0

        if is_maximizer:
            best = -1000

            for possible_field in possible_fields:
                temp_grid[possible_field[0]][possible_field[1]] = "X"
                possible_best = self.minimax(temp_grid, not is_maximizer)
                best = max(best, possible_best)
                temp_grid[possible_field[0]][possible_field[1]] = " "

            return best

        else:
            best = 1000

            for possible_field in possible_fields:
                temp_grid[possible_field[0]][possible_field[1]] = "O"
                possible_best = self.minimax(temp_grid, not is_maximizer)
                best = min(best, possible_best)
                temp_grid[possible_field[0]][possible_field[1]] = " "

            return best

    def get_best_field(self):
        possible_fields = self.get_possible_fields(self.grid)
        temp_grid = deepcopy(self.grid)

        best_state = -1000
        best_field = None
        for possible_field in possible_fields:
            temp_grid[possible_field[0]][possible_field[1]] = "X"
            state = self.minimax(temp_grid, False)
            temp_grid[possible_field[0]][possible_field[1]] = " "


            if state > best_state:
                best_state = state
                best_field = possible_field

        return best_field

    def get_next_win_move(self, player, grid):
        possible_fields = self.get_possible_fields(self.grid)

        # horizontal check
        for i in range(3):
            fields_used_h = []
            count_h = 0
            for j in range(3):
                field = grid[i][j]
                if field == player:
                    fields_used_h.append((i, j))
                    count_h += 1

            if count_h == 2:
                if not (i, 0) in fields_used_h:
                    next_field = i, 0
                elif not (i, 1) in fields_used_h:
                    next_field = i, 1
                else:
                    next_field = i, 2

                if next_field in possible_fields:
                    return next_field

        # vertical check
        for i in range(3):
            fields_used_v = []
            count_v = 0
            for j in range(3):
                field = grid[j][i]
                if field == player:
                    fields_used_v.append((j, i))
                    count_v += 1

            if count_v == 2:
                if not (0, i) in fields_used_v:
                    next_field = 0, i
                elif not (1, i) in fields_used_v:
                    next_field = 1, i
                else:
                    next_field = 2, i

                if next_field in possible_fields:
                    return next_field

        # diagonal check
        fields_used_d = []
        count_d = 0
        for i in range(3):
            field = grid[i][i]
            if field == player:
                fields_used_d.append((i, i))
                count_d += 1

        if count_d == 2:
            if not (0, 0) in fields_used_d:
                next_field = 0, 0
            elif not (1, 1) in fields_used_d:
                next_field = 1, 1
            else:
                next_field = 2, 2

            if next_field in possible_fields:
                return next_field

        fields_used_d = []
        d = 2
        count_d = 0
        for i in range(3):
            field = grid[d][i]
            if field == player:
                fields_used_d.append((d, i))
                count_d += 1

            d -= 1

        if count_d == 2:
            if not (2, 0) in fields_used_d:
                next_field = 2, 0
            elif not (1, 1) in fields_used_d:
                next_field = 1, 1
            else:
                next_field = 0, 2

            return next_field

        return None

    def set_player_move(self, coordinates):
        self.grid[coordinates[0]][coordinates[1]] = "O"

    def set_bot_move(self, coordinates):
        self.grid[coordinates[0]][coordinates[1]] = "X"

    def generate_input(self):

        if self.invalid_input:
            self.invalid_input = False
            field_str = input("Invalid field. Make sure it's in format e.g. 'A1' and try again: ")
        elif self.field_already_used:
            self.field_already_used = False
            field_str = input("Field already used, try again: ")
        else:
            field_str = input("Enter field: ")

        return field_str

    def generate_grid(self):
        os.system("cls")
        format_list = []
        for row in self.grid:
            for field in row:
                format_list.append(field)
        output = """
                 A   B   C
               ------------
            1 ┆  {0} │ {1} │ {2}
              ┆ ───┼───┼───
            2 ┆  {3} │ {4} │ {5}
              ┆ ───┼───┼───
            3 ┆  {6} │ {7} │ {8}
        """.format(*format_list)
        print(output)

    def reset_game(self):
        self.grid = [[" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]]

        self.invalid_input = False
        self.field_already_used = False

    def main_loop(self):
        game_finished = False
        first_run = True

        while True:
            if game_finished:
                game_finished = False
                first_run = True

                input_finished = input("Do you want to restart? (y/n): ")
                if input_finished.lower() in ["yes", "y"]:
                    self.reset_game()
                    continue
                else:
                    for _ in range(2):
                        sys.stdout.write("\x1b[1A")
                        sys.stdout.write("\x1b[2K")
                    print(f"\rExit.")
                    break

            self.generate_grid()

            if first_run:
                first_run = False

                difficulty_str = input("Choose difficulty (0: easy, 1: medium, 2: impossible): ")
                while True:
                    try:
                        difficulty = int(difficulty_str)
                    except ValueError:
                        sys.stdout.write("\x1b[1A")
                        sys.stdout.write("\x1b[2K")
                        difficulty_str = input("Invalid difficulty. Please try again (0: easy, 1: medium, 2: impossible): ")
                    else:
                        sys.stdout.write("\x1b[1A")
                        sys.stdout.write("\x1b[2K")
                        break

            field_str = self.generate_input()

            self.check_input(field_str)
            if self.invalid_input:
                continue

            coordinates = self.get_coordinates(field_str)
            self.check_field(self.grid[coordinates[0]][coordinates[1]])
            if self.field_already_used:
                continue

            self.set_player_move(coordinates)

            is_player_win = self.check_winner("O", self.grid)
            if is_player_win:
                self.generate_grid()
                print(f"You win! :D")
                game_finished = True
                continue

            possible_fields = self.get_possible_fields(self.grid)
            if not possible_fields:
                self.generate_grid()
                print(f"Draw!")
                game_finished = True
                continue

            if difficulty == 0:
                bot_field = random.choice(possible_fields)

            elif difficulty == 1:
                next_move_win = self.get_next_win_move("O", self.grid)

                if next_move_win:
                    bot_field = next_move_win
                else:
                    bot_field = random.choice(possible_fields)

            elif difficulty == 2:
                bot_field = self.get_best_field()

            else:
                raise ValueError("Difficulty not found")

            self.set_bot_move((bot_field[0], bot_field[1]))
            is_bot_win = self.check_winner("X", self.grid)
            if is_bot_win:
                self.generate_grid()
                print(f"You lose! :(")
                game_finished = True
                continue


tic_tac_toe = TicTacToe()

if __name__ == "__main__":
    try:
        tic_tac_toe.main_loop()
    except KeyboardInterrupt:
        sys.stdout.write("\x1b[2K")
        print("\rExit.")
