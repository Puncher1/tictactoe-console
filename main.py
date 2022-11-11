import os
import random


class TicTacToe:

    def __init__(self):
        self.grid = [[" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]]

        self.invalid_input = False
        self.field_already_used = False

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

    def get_possible_fields(self):
        possible_fields = []
        for i, row in enumerate(self.grid):
            for j, field in enumerate(row):
                if field == " ":
                    possible_fields.append((i, j))
        return possible_fields

    def get_random_coordinates(self, possible_fields):
        rand_field = random.choice(possible_fields)
        return rand_field[0], rand_field[1]

    def check_input(self, input_str):
        if not len(input_str) == 2:
            self.invalid_input = True
            return

        letter = input_str[0]
        num = input_str[1]

        if letter not in ["A", "B", "C"] or num not in ["1", "2", "3"]:
            self.invalid_input = True

    def check_field(self, field):
        if field != " ":
            self.field_already_used = True

    def get_winner(self):

        # horizontal check
        for i in range(3):
            O_count_h = 0
            X_count_h = 0
            for j in range(3):
                field = self.grid[i][j]
                if field == "O":
                    O_count_h += 1

                if field == "X":
                    X_count_h += 1

            if O_count_h == 3:
                return "O"
            elif X_count_h == 3:
                return "X"

        # vertical check
        for i in range(3):
            O_count_v = 0
            X_count_v = 0
            for j in range(3):
                field = self.grid[j][i]
                if field == "O":
                    O_count_v += 1

                if field == "X":
                    X_count_v += 1

            if O_count_v == 3:
                return "O"
            elif X_count_v == 3:
                return "X"

        # diagonal check
        O_count_d = 0
        X_count_d = 0
        for i in range(3):
            field = self.grid[i][i]
            if field == "O":
                O_count_d += 1

            if field == "X":
                X_count_d += 1

        if O_count_d == 3:
            return "O"
        elif X_count_d == 3:
            return "X"

        d = 2
        O_count_d = 0
        X_count_d = 0
        for i in range(3):
            field = self.grid[d][i]
            if field == "O":
                O_count_d += 1

            if field == "X":
                X_count_d += 1

            d -= 1

        if O_count_d == 3:
            return "O"
        elif X_count_d == 3:
            return "X"


    def set_player_move(self, coordinates):
        self.grid[coordinates[0]][coordinates[1]] = "O"

    def set_bot_move(self, coordinates):
        self.grid[coordinates[0]][coordinates[1]] = "X"

    def generate_input(self):

        if self.invalid_input:
            self.invalid_input = False
            field_str = input("Invalid input. Make sure it's in format e.g. 'A1' and try again: ")
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


    def main_loop(self):
        while True:
            self.generate_grid()
            field_str = self.generate_input()

            self.check_input(field_str)
            if self.invalid_input:
                continue

            coordinates = self.get_coordinates(field_str)
            self.check_field(self.grid[coordinates[0]][coordinates[1]])
            if self.field_already_used:
                continue

            self.set_player_move(coordinates)

            winner = self.get_winner()
            if winner:
                self.generate_grid()
                print(f"{winner} wins!")
                break

            possible_fields = self.get_possible_fields()
            if not possible_fields:
                self.generate_grid()
                print(f"It's a tie!")
                break

            rand_coordinates = self.get_random_coordinates(possible_fields)
            self.set_bot_move(rand_coordinates)

            winner = self.get_winner()
            if winner:
                self.generate_grid()
                print(f"{winner} wins!")
                break



tic_tac_toe = TicTacToe()

if __name__ == "__main__":
    tic_tac_toe.main_loop()
