class Ship(object):
    """
    Representing the ships that are placed on the board
    """

    def __init__(self,
                 coord_start: tuple,
                 coord_end: tuple):
        """
        Creates a ship given its start and end coordinates on board (the order does not matter)
        :param coord_start: tuple of 2 positive integers representing the starting position of the Ship on the board
        :param coord_end: tuple of 2 positive integers representing the ending position of the Ship on the board
        :raise ValueError: if the ship is neither horizontal nor vertical
        """

        self.x_start, self.y_start = coord_start
        self.x_end, self.y_end = coord_end

        self.x_start, self.x_end = min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        self.y_start, self.y_end = min(self.y_start, self.y_end), max(self.y_start, self.y_end)

        if not self.is_horizontal() and not self.is_vertical():
            raise ValueError("The ship_1 needs to have either a horizontal or a vertical orientation.")

        self.set_coordinates_damages = set()
        self.set_all_coordinates = self.get_all_coordinates()

    def __len__(self):
        return self.length()

    def __repr__(self):
        return f"Ship(start=({self.x_start},{self.y_start}), end=({self.x_end},{self.y_end}))"

    @classmethod
    def get_ship_from_str_coordinates(cls, coord_str_start: str, coord_str_end: str) -> 'Ship':
        from battleship.convert import get_tuple_coordinates_from_str
        return cls(coord_start=get_tuple_coordinates_from_str(coord_str_start),
                   coord_end=get_tuple_coordinates_from_str(coord_str_end))

    def is_vertical(self) -> bool:
        """
        :return: True if and only if the direction of the ship is vertical
        """
        if (self.x_start == self.x_end): #check if row coordinates are the same (ie if the ship is horizontal)
            return True
        else:
            return False #if they are not the same, ship is not horizontal
        # TODO

    def is_horizontal(self) -> bool:
        """
        :return: True if and only if the direction of the ship is horizontal
        """

        if (self.y_start == self.y_end): #check if row coordinates are the same (ie if the ship is horizontal)
            return True
        else: #if they are not the same, ship is not horizontal
            return False
        # TODO

    def length(self) -> int:
        """"
        :return: The number of positions the ship takes on Board
        """
        length = abs(self.x_start-self.x_end + self.y_start-self.y_end) + 1
        #if ship is horizontal, ystart-yend = 0. If ship is vertical, xstart-xend =0.
        #either way the formula above calculates the lenth of the ship by taking the absolute distance between
        #the two differing coordinates (x or y) and adding 1. The 1 is added because e.g.: 5-3 is 2, but the ship ranges from 3 to 5 inclusive
        #so the length is 3
        return length
        # TODO

    def is_on_coordinate(self,
                         coord_x: int,
                         coord_y: int
                         ) -> bool:
        """
        :param coord_x: integer representing the projection of a coordinate on the x-axis
        :param coord_y: integer representing the projection of a coordinate on the y-axis
        :return: True if and only if the ship if (coord_x, coord_y) is one of the coordinates of the ship
        """
        if (self.x_start <= coord_x <=self.x_end) and (self.y_start <= coord_y <= self.y_end):
        #class constructor automatically orders x_start and x_end s.t. xstart<xend. You only need to check if
        #coord_x or y are between their corresponding start and end values to see if its on the ship
            return True
        else:
            return False
        # TODO

    def gets_damage_at(self,
                       coord_damage_x: int,
                       coord_damage_y: int
                       ) -> None:
        """
        The ship gets damaged at the point (coord_damage_x, coord_damage_y)
        :param coord_damage_x: integer representing the projection of a coordinate on the x-axis
        :param coord_damage_y: integer representing the projection of a coordinate on the y-axis
        """
        if self.is_on_coordinate(coord_damage_x, coord_damage_y): #checks if input coordinates are in ship, if so, adds to damage set
            self.set_coordinates_damages.add((coord_damage_x, coord_damage_y))

        # TODO

    def is_damaged_at(self,
                      coord_x: int,
                      coord_y: int,
                      ) -> bool:
        """
        :param coord_x: integer representing the projection of a coordinate on the x-axis
        :param coord_y: integer representing the projection of a coordinate on the y-axis
        :return True if and only if the ship is damaged at (coord_x, coord_y)
        """
        coord = (coord_x,coord_y)
        if coord in self.set_coordinates_damages:
            return True
        else:
            return False
        # TODO

    def number_damages(self) -> int:
        """
        :return: The total number of coordinates at which the ship is damaged
        """
        return len(self.set_coordinates_damages)#length of set_coordinates_damages is the number of damaged coordinates

    def has_sunk(self) -> bool:
        """
        :return: True if and only if ship is damaged at all its positions
        """
        if self.number_damages() == self.length():
            return True
        else:
            return False
        #as set_coordinates_damages is a set, it cannot have repeating values. If its length = length of the ship,
        #the ship has sunk. Therefore returns True, else False

    def get_all_coordinates(self) -> set:
        """
        :return: A set containing only all the coordinates of the ship
        """
        coords = set()

        for i in range (self.x_start,self.x_end+1):
            for j in range (self.y_start,self.y_end+1):
                t = (i,j)
                coords.add(t)

        return coords

        # TODO

    def is_near_coordinate(self, coord_x: int, coord_y: int) -> bool:
        """
        Tells if the ship is near a coordinate or not.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------


        :param coord_x: integer representing the projection of a coordinate on the x-axis
        :param coord_y: integer representing the projection of a coordinate on the y-axis
        :return: True if and only if (coord_x, coord_y) is at a distance of 1 of the ship OR is at the
        corner of the ship
        """
        return self.x_start - 1 <= coord_x <= self.x_end + 1 \
               and self.y_start - 1 <= coord_y <= self.y_end + 1

    def is_near_ship(self, other_ship: 'Ship') -> bool:
        """
        :param other_ship: other object of class Ship
        :return: False if and only if there is a coordinate of other_ship that is near this ship.
        """
        #Starts by scanning over each coordinate of self ship
        for x in range(self.x_start,self.x_end+1):
            for y in range(self.y_start,self.y_end+1):
                #if any of these coordiates are near another ship,
                #print(f"C1 {x},{y}")
                if self.is_near_coordinate(x,y):
                    #print("ship nearby")
                    #scans the surrounding coordinates to see if any of them are on other ship
                    for x2 in range(x-1,x+2):
                        for y2 in range(y-1,y+2):
                            #if the surrounding coordinate is on other ship, the two ships are
                            #near each other so returns true
                            #print(f"C2 {x2},{y2}")
                            if (other_ship.is_on_coordinate(x2,y2)):
                                #print(f"other ship found: {x2},{y2}")
                                return True
        #if the whole scaning process finds that none of the surrounding coordinates are on
        #other ship, the ships must not be close to each other, so returns false.
        #sadly, is_near_coordinate does not return coordinates and does not check for specific ships, so
        #there are a lot of 'false positives' where the method considers parts of the self ship as a nearby ship
        #which increases processing steps, however the method does its job without fail
        return False




if __name__ == '__main__':
    # SANDBOX for you to play and test your functions

    ship = Ship(coord_start=(4, 2), coord_end=(4, 4))
    ship2 = Ship(coord_start=(5,5), coord_end=(5,8))
    #print(ship.is_near_ship(ship2))
    #print(ship.is_near_coordinate(5, 3))
    #ship.gets_damage_at(4, 4)
    #print(ship.is_damaged_at(4,3))
    #ship.gets_damage_at(10, 3)
    #print(ship.is_damaged_at(4, 3), ship.is_damaged_at(5, 3), ship.is_damaged_at(10, 3))

    #ship_2 = Ship(coord_start=(4, 1), coord_end=(4, 5))
    #print(ship.is_near_ship(ship_2))
