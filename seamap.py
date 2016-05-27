from ships import Ship
import copy
import random
from time import sleep

class Map:
    def __init__(self, size=10):
        # Make a 2D array, size x size
        self.map = [[0 for column in range(size)] for row in range(size)]
        # Make a list of the ships that can be placed on this map
        self.ships = []
        # self.ships = [Ship("Aircraft Carrier"),
        #               Ship("Battleship"),
        #               Ship("Submarine"),
        #               Ship("Destroyer"),
        #               Ship("Patrol Boat"),
        #               Ship("Patrol Boat")]
        self.hits = []
        self.dirlist = ["up", "down", "left", "right"]

    # X AND Y ARE ALWAYS 0:len(self.map) (e.g. 0-9)
    def coord_okay(self, x, y):
        rng = range(len(self.map))
        if x in rng and y in rng:
            return True
        else:
            return False

    # Returns what is on a particular tile
    def get_occupant(self, x, y):
        if not self.coord_okay(x, y):
            return None
        occupant = self.map[x][y]
        return occupant

    def is_water(self, x, y):
        occupant = self.get_occupant(x, y)
        if occupant == 0:
            return True
        else:
            return False

    def is_strikeable(self, x, y):
        occupant = self.get_occupant(x, y)
        if occupant in ["h", "m", None]:
            return False
        else:
            return True

    def is_hit(self, x, y):
        occupant = self.get_occupant(x, y)
        if occupant == "h":
            return True
        else:
            return False

    def is_miss(self, x, y):
        occupant = self.get_occupant(x, y)
        if occupant == "m":
            return True
        else:
            return False

    def is_clear_lane(self, x, y, direction, length):
        row = x
        col = y
        for i in range(length):
            if direction == "up":
                row = x - i
            elif direction == "down":
                row = x + i
            elif direction == "left":
                col = y - i
            elif direction == "right":
                col = y + i
            if not self.is_water(row, col):
                return False
        return True

    def get_lane_occupants(self, x, y, direction, length):
        row = x
        col = y
        occupants = []
        for i in range(length):
            if direction == "up":
                row = x - i
            elif direction == "down":
                row = x + i
            elif direction == "left":
                col = y - i
            elif direction == "right":
                col = y + i
            occupants.append(self.get_occupant(row, col))
        return occupants

    def place_ship(self, ship, x, y, direction):
        if not self.is_clear_lane(x, y, direction, ship.length):
            return False
        row = x
        col = y
        for i in range(ship.length):
            if direction == "up":
                row = x - i
            elif direction == "down":
                row = x + i
            elif direction == "left":
                col = y - i
            elif direction == "right":
                col = y + i
            self.map[row][col] = ship
            ship.coords.append((row, col))
        self.ships.append(ship)
        return True

    def place_strike(self, x, y):
        if not self.is_strikeable(x, y):
            return None
        occupant = self.get_occupant(x, y)
        if type(occupant) == Ship:
            occupant.hit(x, y)
            self.map[x][y] = "h"
            if not occupant.alive:
                self.ships.remove(occupant)
                return occupant.name
            return "hit"
        else:
            self.map[x][y] = "m"
            return "miss"

    def get_hit_coords(self):
        hitlist = []
        row = 0
        col = 0
        for x in self.map:
            for y in x:
                if y == "h":
                    hitlist.append((row, col))
                col += 1
            row += 1
            col = 0
        return hitlist

    def get_coord_cardinal(self, x, y, direction="random"):
        if direction == "random":
            direction = random.choice(self.dirlist)
        if direction == "up":
            x -= 1
        elif direction == "down":
            x += 1
        elif direction == "left":
            y -= 1
        elif direction == "right":
            x += 1
        return (x, y)

    # Deprecated
    def get_possible_ships1(self, x, y, length):
        if not self.coord_okay(x, y):
            return {}
        occupantsv = {}
        occupantsh = {}
        for i in range(length):
            occupantsv[i] = self.get_lane_occupants(x - i, y, "down", length)
        for i in range(length):
            occupantsh[i] = self.get_lane_occupants(x, y - i, "right", length)
        # for i in occupantsv:
        #

    # TODO: Slice up the dictionaries so that they only consist of contiguous
    # ranges where from the center (hit) they contain neither "m" nor None.
    # A bit tough especially since the dicts won't be ordered.
    # ex:      this... {(4, 7): 0, (5, 7): 'm', (6, 7): 'h', (7, 7): 0, (8, 7): 'h'}
    # turns to this... {(6, 7): 'h', (7, 7): 0, (8, 7): 'h'}
    def get_possible_hit_ships(self, x, y):
        if not self.is_hit(x, y):
            return None
        row = x
        col = y
        shiplengths = [i.length for i in self.ships]
        maxlength = max(shiplengths)
        occdictv = {}
        occdicth = {}
        coordlistv = []
        coordlisth = []
        occlistv = []
        occlisth = []
        for i in range((x - (maxlength - 1)), (x + maxlength)):
            row = i
            occdictv[(row, col)] = self.get_occupant(row, col)
            coordlistv.append((row, col))
            occlistv.append(self.get_occupant(row, col))
        for i in range((y - (maxlength - 1)), (y + maxlength)):
            col = i
            occdicth[(row, col)] = self.get_occupant(row, col)
            coordlisth.append((row, col))
            occlisth.append((row, col))
            occlisth.append(self.get_occupant(row, col))
        # print(occdictv)
        # print(occdicth)



class MapABC:
    def __init__(self):
        self.map = {"A": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "C": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "D": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "E": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "F": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "G": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "H": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "I": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "J": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.ships = []
        self.letlist = sorted([i for i in self.map])
        self.numlist = [i + 1 for i in range(len(self.map["A"]))]
        self.dirlist = ["up", "down", "left", "right"]

    # Place a ship. TODO: rewrite using .radar()/.okay_to_place()
    # ship:         Ship()  e.g. Ship("Battleship")
    # letter:       Str     e.g. 'B'
    # number:       Int     e.g. 10
    # direction:    Str     e.g. "down"
    def place_ship(self, ship, letter, number, direction):
        self.ships.append(ship.name)
        letlist = sorted([i for i in self.map])
        print("\nShip: {0}, Length: {1}".format(ship.name, ship.length))
        letterindex = letlist.index(letter)

        if direction == "down":
            if ship.length <= len(letlist[letterindex:]):
                print("Placing {}...".format(ship.name))
                letplace = letterindex
                mapbackup = copy.deepcopy(self.map)
                for num in range(ship.length):
                    occupant = self.map[letlist[letplace]][number - 1]
                    if occupant == 0:
                        self.map[letlist[letplace]][number - 1] = ship.name
                        letplace += 1
                    else:
                        self.map = mapbackup
                        print("Ship would collide with already placed {}".format(occupant))
            else:
                print("Ship would fall off the game board.")

        if direction == "up":
            if ship.length <= len(letlist[:letterindex + 1]):
                print("Placing {}...".format(ship.name))
                letplace = letterindex
                mapbackup = copy.deepcopy(self.map)
                for num in range(ship.length):
                    occupant = self.map[letlist[letplace]][number - 1]
                    if occupant == 0:
                        self.map[letlist[letplace]][number - 1] = ship.name
                        letplace -= 1
                    else:
                        self.map = mapbackup
                        print("Ship would collide with already placed {}".format(occupant))
            else:
                print("Ship would fall off the game board.")

        if direction == "right":
            if ship.length <= 11 - number:
                print("Placing {}...".format(ship.name))
                numplace = number - 1
                mapbackup = copy.deepcopy(self.map)
                for num in range(ship.length):
                    occupant = self.map[letter][numplace]
                    if occupant == 0:
                        self.map[letter][numplace] = ship.name
                        numplace += 1
                    else:
                        self.map = mapbackup
                        print("Ship would collide with already placed {}".format(occupant))
            else:
                print("Ship would fall off the game board.")

        if direction == "left":
            if ship.length <= number:
                print("Placing {}...".format(ship.name))
                numplace = number - 1
                mapbackup = copy.deepcopy(self.map)
                for num in range(ship.length):
                    occupant = self.map[letter][numplace]
                    if occupant == 0:
                        self.map[letter][numplace] = ship.name
                        numplace -= 1
                    else:
                        self.map = mapbackup
                        print("Ship would collide with already placed {}".format(occupant))
            else:
                print("Ship would fall off the game board.")

    def display_map(self, playerstring=""):
        mapstrings = copy.deepcopy(self.map)
        print("\n\n{}Current Map:".format(playerstring))
        for row in mapstrings:
            for column in range(10):
                mapstrings[row][column] = str(mapstrings[row][column])[0]
        for row in mapstrings:
            for column in range(10):
                if mapstrings[row][column] == "0":
                    mapstrings[row][column] = "."
        for row in sorted(mapstrings):
            print("{0} |".format(row), *mapstrings[row])
        print("  ---------------------")
        print("    1 2 3 4 5 6 7 8 9 10")

    def display_strike_map(self, playerstring=""):
        mapstrings = copy.deepcopy(self.map)
        print("\n\n{}Current Strike Map:".format(playerstring))
        for row in mapstrings:
            for column in range(10):
                if mapstrings[row][column] != "m" and mapstrings[row][column] != "h":
                    mapstrings[row][column] = "."
        for row in sorted(mapstrings):
            print("{0} |".format(row), *mapstrings[row])
        print("  ---------------------")
        print("    1 2 3 4 5 6 7 8 9 10")

    def place_strike(self, letter, number):
        print("\n")
        if letter in self.map and number <= 10:
            occupant = self.map[letter][number - 1]
            if occupant == "m":
                print("Location already struck (it was a miss).")
                return "hot water"
            elif occupant == "h":
                print("Location already struck (it was a hit).")
                return "debris"
            elif occupant == 0:
                self.map[letter][number - 1] = "m"
                return "water"
            else:
                self.map[letter][number - 1] = "h"
                return occupant
        else:
            print("Invalid coordinate.")
            return "nothing"

    def place_strike_random(self):
        occupant = "h"
        while occupant == "h" or occupant == "m":
            randlet = random.choice(self.letlist)
            randnum = random.choice(self.numlist)
            occupant = self.map[randlet][randnum - 1]
        self.place_strike(randlet, randnum)

    def radar(self, letter, number):
        print("\n...blip...blip...blip...")
        if letter in self.map and number <= 10:
            occupant = self.map[letter][number - 1]
            if occupant == "m":
                return "hot water"
            elif occupant == "h":
                return "debris"
            elif occupant == 0:
                return "water"
            else:
                return occupant
        else:
            print("Invalid coordinate.")
            return "nothing"

    def okay_to_place(self, ship, letter, number, direction="down"):
        print("\nRadio:         '{0}, please confirm trajectory to {1}{2}, going {3}.'".format(ship.name, letter, number, direction))
        occlist = []
        letterindex = self.letlist.index(letter)
        if direction == "down":
            if ship.length <= 10 - letterindex:
                for n in range(ship.length):
                    occupant = self.map[self.letlist[letterindex + n]][number - 1]
                    occlist.append(occupant)
            else:
                print("Fleet Control: 'Trajectory obstructed.'")
                return False
        if direction == "up":
            if ship.length <= letterindex + 1:
                for n in range(ship.length):
                    occupant = self.map[self.letlist[letterindex - n]][number - 1]
                    occlist.append(occupant)
            else:
                print("Fleet Control: 'Trajectory obstructed.'")
                return False
        if direction == "right":
            if ship.length <= 11 - number:
                for n in range(ship.length):
                    occupant = self.map[letter][number + n - 1]
                    occlist.append(occupant)
            else:
                print("Fleet Control: 'Trajectory obstructed.'")
                return False
        if direction == "left":
            if ship.length <= number:
                for n in range(ship.length):
                    occupant = self.map[letter][number - n - 1]
                    occlist.append(occupant)
            else:
                print("Fleet Control: 'Trajectory obstructed.'")
                return False
        for occ in occlist:
            if occ != 0:
                print("Fleet Control: 'Trajectory obstructed.'")
                return False
        print("Fleet Control: 'Trajectory clear.'")
        return True

    def populate_random(self, anum=1, bnum=1, snum=1, dnum=1, pnum=2):
        a = Ship("Aircraft Carrier")
        b = Ship("Battleship")
        s = Ship("Submarine")
        d = Ship("Destroyer")
        p = Ship("Patrol Boat")
        shipnumdict = {a: anum, b: bnum, s: snum, d: dnum, p: pnum}

        for ship in shipnumdict:
            shipcount = shipnumdict[ship]
            while shipcount > 0:
                randlet = random.choice(self.letlist)
                randnum = random.choice(self.numlist)
                randdir = random.choice(self.dirlist)
                if self.okay_to_place(ship, randlet, randnum, randdir):
                    print("\nFleet Control: 'Placing {0} at {1}{2} going {3}.''".format(ship.name, randlet, randnum, randdir))
                    self.place_ship(ship, randlet, randnum, randdir)
                    shipcount -= 1
                    print("{0} {1} left to place randomly...".format(shipcount, ship.name))


if __name__ == "__main__":
    m = Map()
    b = Ship("Battleship")
    b2 = Ship("Battleship")
    p = Ship("Patrol Boat")
    print(m.coord_okay(0,8))
    print(m.get_occupant(0,0))
    # m.map[5][5] = "x"
    for row in m.map:
        print(row)
    print(m.is_clear_lane(3, 3, "down", 5))
    print(m.is_clear_lane(3, 3, "left", 5))
    print(m.is_clear_lane(5, 3, "right", 5))
    print(m.get_lane_occupants(3, 3, "down", 5))
    print(m.get_lane_occupants(3, 3, "left", 5))
    print(m.get_lane_occupants(5, 3, "right", 5))
    print(m.place_ship(b, 7, 7, "up"))
    print(m.place_ship(b2, 5, 5, "left"))
    print(m.place_ship(p, 2, 2, "right"))
    for row in m.map:
        print(row)
    print(b.coords)
    print(type(b) == Ship)
    m.place_strike(6, 7)
    for row in m.map:
        print(row)
    print(b.coords)
    print(b.damage)
    print(b.get_hull_remaining())
    print(b.alive)
    print(m.ships)
    print(m.place_strike(7, 7))
    print(m.place_strike(5, 7))
    print(m.place_strike(4, 7))
    for row in m.map:
        print(row)
    print(b.coords)
    print(b.damage)
    print(b.get_hull_remaining())
    print(b.alive)
    print(m.ships)
    print(m.get_hit_coords())
    # for i in m.get_possible_ships(4, 4, 5):
    #     # print("\n")
    #     print(i)
    print(m.get_possible_hit_ships(6, 7))
