from player import Player
from seamap import Map
from ships import Ship
import random

class Robot(Player):
    def __init__(self, difficulty="easy"):
        super().__init__("Admiral Rowe Bott")
        self.difficulty = difficulty
        self.populate_random()

    def take_turn(self):
        if self.difficulty == "easy":
            self.opponent.place_strike_random()
        # TODO: on medium: place strikes near hits, until a ship has sunk
        # IN PROGRESS: set up a different function to analyze strike map instead
        if self.difficulty == "medium":
            hits = self.get_opponent_hits()

        # TODO: on hard: place strikes in cardinal directions next to hits, then
        #                follow line of hits backwards and forwards until sunk

    def get_opponent_hits(self):
        hits = []
        for letter in self.opponent.seamap:
            for column in self.opponent.seamap[letter]:
                if column == "h":
                    hits.append([letter, column])
        return hits

    def get_placeable_cardinal(self, letter, number, direction="none"):
        letcount = len(self.opponent.letlist)
        numcount = len(self.opponent.numlist)
        newlet = letter
        newletindex = self.opponent.letlist.index(letter)
        newnum = number

        if direction == "none":
            direction = random.choice(self.dirlist)

        if direction == "up":
            newletindex -= 1
        elif direction == "down":
            newletindex += 1
        elif direction == "left":
            newnum -= 1
        elif direction == "right":
            newnum += 1

        if not (0 <= newletindex < letcount):
            print("Letter out of range.")
            return None
        else:
            newlet = self.opponent.letlist[newletindex]

        if not (0 < newnum <= numcount):
            print("Number out of range.")
            return None

        radar = self.opponent.radar(newlet, newnum)
        if radar in ["hot water", "debris", "nothing"]:
            print("Unable to place at {0}{1} - {2} present.".format(newlet, newnum, radar))
            return None
        else:
            return [newlet, newnum]

    def get_opponent_cardinal(self, letter, number, direction):
        letcount = len(self.opponent.letlist)
        numcount = len(self.opponent.numlist)
        newlet = letter
        newletindex = self.opponent.letlist.index(letter)
        newnum = number

        if direction == "up":
            newletindex -= 1
        elif direction == "down":
            newletindex += 1
        elif direction == "left":
            newnum -= 1
        elif direction == "right":
            newnum += 1

        if not (0 <= newletindex < letcount):
            print("Letter out of range.")
            return None
        else:
            newlet = self.opponent.letlist[newletindex]

        if not (0 < newnum <= numcount):
            print("Number out of range.")
            return None

        radar = self.opponent.radar(newlet, newnum)
        return [radar, newlet, newnum]

    # TODO: look through possible lengths using get_spaces()
    def is_possible_ship(self, letter, number, direction):
        lengths = []
        for shipname in self.opponent.ships:
            if self.opponent.ships[shipname] > 0:
                lengths.append(Ship(shipname).length)
        if len(lengths) == 0:
            print("No opponent ships still standing.")
            return False
        first = self.get_opponent_cardinal(letter, number, direction)
        occupants = []
        newnum = number
        newlet = letter
        for i in range(max(lengths)):
            if direction == "right":
                occupant = self.get_opponent_cardinal(newlet, newnum+i, direction)
            if direction == "left":
                occupant = self.get_opponent_cardinal(newlet, newnum-i, direction)
            # if direction == "up":
            #     occupant = self.get_opponent_cardinal(newlet, newnum, direction)
            # if direction == "down":
            #     occupant = self.get_opponent_cardinal(newlet, newnum, direction)


if __name__ == "__main__":
    r = Robot()
    p = Player("Keegan")
    r.add_opponent(p)
    p.populate_random()
    for i in range(10):
        r.take_turn()
    p.display_map()
    p.display_strike_map()
    r.display_map()

    p.place_strike("E", 6)
    p.display_map()
    # print(r.get_space_cardinal("J", 10, "down"))
    r.is_possible_ship("A", 1, "down")
