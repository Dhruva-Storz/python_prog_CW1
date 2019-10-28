from typing import List, Tuple

import random

from battleship.ship import Ship

# from ship import Ship

OFFSET_UPPER_CASE_CHAR_CONVERSION = 64


class Board(object):
    """
    Class representing the board of the player. Interface between the player and its ships.
    """
    SIZE_X = 10  # length of the rectangular board, along the x axis
    SIZE_Y = 10  # length of the rectangular board, along the y axis

    # dict: length -> number of ships of that length
    DICT_NUMBER_SHIPS_PER_LENGTH = {1: 1,
                                    2: 1,
                                    3: 1,
                                    4: 1,
                                    5: 1}

    def __init__(self,
                 list_ships: List[Ship]):
        """
        :param list_ships: list of ships for the board.
        :raise ValueError if the list of ships is in contradiction with Board.DICT_NUMBER_SHIPS_PER_LENGTH.
        :raise ValueError if there are some ships that are too close from each other
        """

        self.list_ships = list_ships
        self.set_coordinates_previous_shots = set()

        if not self.lengths_of_ships_correct():
            total_number_of_ships = sum(self.DICT_NUMBER_SHIPS_PER_LENGTH.values())

            error_message = f"There should be {total_number_of_ships} ships in total:\n"

            for length_ship, number_ships in self.DICT_NUMBER_SHIPS_PER_LENGTH.items():
                error_message += f" - {number_ships} of length {length_ship}\n"

            raise ValueError(error_message)

        if self.are_some_ships_too_close_from_each_other():
            raise ValueError("There are some ships that are too close from each other.")

    def has_no_ships_left(self) -> bool:
        """
        :return: True if and only if all the ships on the board have sunk.
        """
        # If there is a single ship that hasnt sunk, returns false
        for Ship in list_ships:
            if not Ship.has_sunk():
                return false
        # if the code can go through the loop without returning false, then all ships have sunk
        return True

    def is_attacked_at(self, coord_x: int, coord_y: int) -> Tuple[bool, bool]:
        """
        The board receives an attack at the position (coord_x, coord_y).
        - if there is no ship at that position -> nothing happens
        - if there is a ship at that position -> it is damaged at that coordinate

        :param coord_x: integer representing the projection of a coordinate on the x-axis
        :param coord_y: integer representing the projection of a coordinate on the y-axis
        :return: a tuple of bool variables (is_ship_hit, has_ship_sunk) where:
                    - is_ship_hit is True if and only if the attack was performed at a set of coordinates where an
                    opponent's ship is.
                    - has_ship_sunk is True if and only if that attack made the ship sink.
        """
        # default values
        is_ship_hit = False
        has_ship_sunk = False

        for ship in self.list_ships:
            if ship.is_on_coordinate(coord_x, coord_y):
                is_ship_hit = True
                ship.gets_damage_at(coord_x, coord_y)
                if ship.has_sunk():
                    has_ship_sunk = True

        return (is_ship_hit, has_ship_sunk)

    def print_board_with_ships_positions(self) -> None:
        array_board = [[' ' for _ in range(self.SIZE_X)] for _ in range(self.SIZE_Y)]

        for x_shot, y_shot in self.set_coordinates_previous_shots:
            array_board[y_shot - 1][x_shot - 1] = 'O'

        for ship in self.list_ships:
            if ship.has_sunk():
                for x_ship, y_ship in ship.set_all_coordinates:
                    array_board[y_ship - 1][x_ship - 1] = '$'
                continue

            for x_ship, y_ship in ship.set_all_coordinates:
                array_board[y_ship - 1][x_ship - 1] = 'S'

            for x_ship, y_ship in ship.set_coordinates_damages:
                array_board[y_ship - 1][x_ship - 1] = 'X'

        board_str = self._get_board_string_from_array_chars(array_board)

        print(board_str)

    def print_board_without_ships_positions(self) -> None:
        array_board = [[' ' for _ in range(self.SIZE_X)] for _ in range(self.SIZE_Y)]

        for x_shot, y_shot in self.set_coordinates_previous_shots:
            array_board[y_shot - 1][x_shot - 1] = 'O'

        for ship in self.list_ships:
            if ship.has_sunk():
                for x_ship, y_ship in ship.set_all_coordinates:
                    array_board[y_ship - 1][x_ship - 1] = '$'
                continue

            for x_ship, y_ship in ship.set_coordinates_damages:
                array_board[y_ship - 1][x_ship - 1] = 'X'

        board_str = self._get_board_string_from_array_chars(array_board)

        print(board_str)

    def _get_board_string_from_array_chars(self, array_board: List[List[str]]) -> str:
        list_lines = []

        array_first_line = [chr(code + OFFSET_UPPER_CASE_CHAR_CONVERSION) for code in range(1, self.SIZE_X + 1)]
        first_line = ' ' * 6 + (' ' * 5).join(array_first_line) + ' \n'

        for index_line, array_line in enumerate(array_board, 1):
            number_spaces_before_line = 2 - len(str(index_line))
            space_before_line = number_spaces_before_line * ' '
            list_lines.append(f'{space_before_line}{index_line} |  ' + '  |  '.join(array_line) + '  |\n')

        line_dashes = '   ' + '-' * 6 * self.SIZE_X + '-\n'

        board_str = first_line + line_dashes + line_dashes.join(list_lines) + line_dashes

        return board_str

    def lengths_of_ships_correct(self) -> bool:
        """
        :return: True if and only if there is the right number of ships of each length, according to
        Board.DICT_NUMBER_SHIPS_PER_LENGTH
        """
        freq1 = 0
        freq2 = 0
        freq3 = 0
        freq4 = 0
        freq5 = 0
        for ship in self.list_ships:
            if (ship.length() == 1):
                freq1 += 1
            elif (ship.length() == 2):
                freq2 += 1
            elif (ship.length() == 3):
                freq3 += 1
            elif (ship.length() == 4):
                freq4 += 1
            elif (ship.length() == 5):
                freq5 += 1
            else:
                # ship cannot be more than 5 coords large
                return False

        if (
                freq1 == self.DICT_NUMBER_SHIPS_PER_LENGTH[1]
                and freq2 == self.DICT_NUMBER_SHIPS_PER_LENGTH[2]
                and freq3 == self.DICT_NUMBER_SHIPS_PER_LENGTH[3]
                and freq4 == self.DICT_NUMBER_SHIPS_PER_LENGTH[4]
                and freq5 == self.DICT_NUMBER_SHIPS_PER_LENGTH[5]
        ):
            return True
        else:
            return False

        # TODO

    def are_some_ships_too_close_from_each_other(self) -> bool:
        """
        :return: True if and only if there are at least 2 ships on the board that are near each other.
        """
        # loop below runs through all permutations of ship pairs (avoiding repeats) and
        # runs is_near_ship on each pair, counting to 2

        for ship1 in self.list_ships:
            for ship2 in self.list_ships[self.list_ships.index(ship1) + 1:]:
                # print(f'{list_ships.index(ship1)},{list_ships.index(ship2)}')
                if ship1.is_near_ship(ship2):
                    return True

        return False


class BoardAutomatic(Board):
    def __init__(self):
        super().__init__(list_ships=self.generate_ships_automatically())

    def ships_too_close(self, ship_list) -> bool:
        # copy of method defined in board that takes a list of ships and checks if more than 2 are
        # near each other
        for ship1 in ship_list:
            for ship2 in ship_list[ship_list.index(ship1) + 1:]:
                if ship1.is_near_ship(ship2):
                    return True

        return False

    def generate_ship(self, size, taken_coordinates) -> Ship:
        # Method that generates a ship of specific size, while making sure it does not conflict
        # with the coordinates of other ships defined in an array called taken_coordinates.

        # Loops until it finds a ship that fits all the selection criteria (coordinates in bounds of board, no conflicts)

        while (1):
            # seedx and seedy are random coordinates that act as seed from which ship grows either backwards or downwards
            seedx = random.randint(1, 10)
            seedy = random.randint(1, 10)
            # array that stores coordinates of ship so they can be checked against taken_coordinates later
            ship_coords = []
            # offset is the offset from seed representing the size of the ship
            offset = size - 1

            # first randomly selects vertical or horizontal
            if random.choice([True, False]):  # True = Horizontal, False = Vertical
                if 1 <= seedx - offset <= 9:  # checks if ships start position (seed - offset) is on the board
                    # defines start and end coordinates, and adds them to ship_coords
                    xstart = seedx - offset
                    xend = seedx
                    ystart = seedy
                    yend = seedy
                    for coord in range((seedx - offset), seedx + 1):
                        coordinates = (coord, seedy)
                        ship_coords.append(coordinates)
                else:  # start coordinate for ship is outside board, starts loop again
                    continue
            else:
                if 1 <= seedy - offset <= 9:  # checks if ships start position (seed - offset) is on the board
                    # defines start and end coordinates, and adds them to ship_coords
                    xstart = seedx
                    xend = seedx
                    ystart = seedy - offset
                    yend = seedy
                    for coord in range((seedy - offset), seedy + 1):
                        coordinates = (seedx, coord)
                        ship_coords.append(coordinates)
                else:  # start coordinate for ship is outside board, starts loop again
                    continue

            # checks if coordinates of ship conflict with other previously created ships
            coords_taken = False
            for coord in ship_coords:
                if coord in taken_coordinates:
                    coords_taken = True

            if not coords_taken:  # if no conflict exists, creates ship and adds coordinates to taken_coordinates
                for coord in ship_coords:
                    taken_coordinates.add(coord)
                GeneratedShip = Ship(coord_start=(xstart, ystart), coord_end=(xend, yend))
                break  # selection criteria met, exits loop
            else:
                continue  # if conflict exists, starts loop again

        return GeneratedShip

    def generate_ships_automatically(self) -> List[Ship]:
        """
        :return: A list of automatically (randomly) generated ships for the board
        """
        # Generates 5 ships of specific lengths, loops until it finds a configuration
        # such that no more than 2 ships are close to each other

        while (1):
            ship_list = []
            occupied_coordinates = set()

            for length, number_ships in self.DICT_NUMBER_SHIPS_PER_LENGTH.items():
                for instances in range(0, number_ships):
                    Generated_ship = self.generate_ship(length, occupied_coordinates)
                    ship_list.append(Generated_ship)

            if self.ships_too_close(ship_list):  # checks if no more than two ships are close to each other
                continue  # continues loop if criterion is not met
            else:
                break  # breaks loop if criterion is met

        return ship_list


if __name__ == '__main__':
    # SANDBOX for you to play and test your functions
    list_ships = [
        Ship(coord_start=(1, 1), coord_end=(1, 1)),
        Ship(coord_start=(3, 3), coord_end=(3, 4)),
        Ship(coord_start=(5, 3), coord_end=(5, 5)),
        Ship(coord_start=(7, 1), coord_end=(7, 4)),
        Ship(coord_start=(9, 3), coord_end=(9, 7)),
    ]

    board = Board(list_ships)
    board.print_board_with_ships_positions()
    board.print_board_without_ships_positions()
    print(board.is_attacked_at(5, 4),
          board.is_attacked_at(10, 9))
    # print(board.set_coordinates_previous_shots)
    # print(f'{board.lengths_of_ships_correct()} length of ships is correct')
    print(board.are_some_ships_too_close_from_each_other())
