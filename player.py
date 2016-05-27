from seamap import Map
from ships import Ship, Buoy
from math import ceil

class Player:
    def __init__(self, playername=""):
        self.seamap = Map()
        self.ships = {"Aircraft Carrier": 1,
                      "Battleship": 1,
                      "Submarine": 1,
                      "Destroyer": 1,
                      "Patrol Boat": 2}
        self.playername = playername
        self.opponent = None
        self.letlist = self.seamap.letlist
        self.numlist = self.seamap.numlist
        self.dirlist = self.seamap.dirlist
        self.buoy = Buoy()

    def add_opponent(self, opponent):
        self.opponent = opponent

    def add_ship(self, shipname):
        if shipname not in self.ships:
            raise ValueError("Ship has invalid name. Choose between " +
            "'Aircraft Carrier', 'Battleship', 'Submarine', 'Destroyer', " +
            "and 'Patrol Boat'.")
        else:
            self.ships[shipname] += 1

    def remove_ship(self, shipname):
        if shipname not in self.ships:
            raise ValueError("Ship has invalid name. Choose between " +
            "'Aircraft Carrier', 'Battleship', 'Submarine', 'Destroyer', " +
            "and 'Patrol Boat'.")
        elif self.ships[shipname] > 0:
            self.ships[shipname] -= 1
        else:
            print("\nNo {} to remove.".format(shipname))

    def place_ship(self, shipname, letter, number, direction):
        self.seamap.place_ship(Ship(shipname), letter, number, direction)

    def place_strike(self, letter, number):
        occupant = self.seamap.place_strike(letter, number)
        print("Opponent struck {}.".format(occupant))
        self.refresh_ships()
        return(occupant)

    def place_strike_random(self):
        self.seamap.place_strike_random()

    def radar(self, letter, number):
        radar = self.seamap.radar(letter, number)
        return radar

    def refresh_ships(self):
        for shipname in self.ships:
            shipcount = 0
            shipsfull = self.ships[shipname]
            for letter in self.seamap.map:
                for column in self.seamap.map[letter]:
                    if column == shipname:
                        shipcount += 1
            shipcount = ceil(shipcount/Ship(shipname).length)
            self.ships[shipname] = shipcount


    def display_map(self):
        self.seamap.display_map("{}'s ".format(self.playername))

    def display_strike_map(self):
        self.seamap.display_strike_map("{}'s ".format(self.playername))

    def populate_random(self):
        anum = self.ships["Aircraft Carrier"]
        bnum = self.ships["Battleship"]
        snum = self.ships["Submarine"]
        dnum = self.ships["Destroyer"]
        pnum = self.ships["Patrol Boat"]
        self.seamap.populate_random(anum, bnum, snum, dnum, pnum)
        self.refresh_ships()

    def is_alive(self):
        self.refresh_ships()
        shipcount = 0
        for ship in self.ships:
            shipcount += self.ships[ship]
        if shipcount == 0:
            return False
        else:
            return True
        print("Something went wrong while counting your ships...")


if __name__ == "__main__":
    p = Player("Keegan")
    p.place_ship("Patrol Boat", "F", 6, "down")
    p.populate_random()
    p.display_map()
    print(p.ships)
    p.place_strike("F", 6)
    print(p.ships)
    p.place_strike("G", 6)
    print(p.ships)
    p.display_map()
    p.display_strike_map()
    print(p.is_alive())
