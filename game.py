from player import Player
from robotplayer import Robot
from seamap import Map
import re
import sys

class Game:
    def __init__(self, p1, p2, difficulty="easy"):
        self.p1 = p1
        self.p2 = p2
        self.p1.add_opponent(p2)
        self.p2.add_opponent(p1)
        self.difficulty = difficulty

    def play(self):
        print("\n\nStarting game with {0} and {1}".format(self.p1.playername, self.p2.playername))
        while self.p1.is_alive() and self.p2.is_alive():
            p1turnfinished = False
            p2turnfinished = False
            self.display_player_view(p1)
            while p1turnfinished == False:
                p1turnfinished = self.play_turn(p1, p2)
            self.display_player_view(p2)
            while p2turnfinished == False:
                p2turnfinished = self.play_turn(p2, p1)

    def display_player_view(self, player):
        print("\n"*100)
        player.opponent.display_strike_map()
        player.display_map()

    def play_turn(self, attacker, defender):
        coord = (input("\n{} - set your target: ".format(attacker.playername))).upper()
        if not (re.match(r'^[A-Z][1-9]$', coord) or re.match(r'^[A-Z]10$', coord)):
            print("Please enter a valid coordinate (e.g. C10).")
            return False
        letter = coord[0]
        number = int(coord[1:])
        occupant = defender.place_strike(letter, number)
        if occupant in ["hot water", "debris", "nothing"]:
            print("\n"*100)
            print("Struck {}, try again.".format(occupant))
            defender.display_strike_map()
            attacker.display_map()
            return False
        print("\n"*100)
        print("Struck {}".format(occupant))
        defender.display_strike_map()
        attacker.display_map()
        return True


if __name__ == '__main__':
    p1 = Player("Keegan")
    p1.populate_random()
    p2 = Player("Aishu")
    p2.populate_random()
    g = Game(p1, p2)
    g.play()
    # p2.display_map()
    # g.play_turn(p1, p2)
    # p2.display_map()
    # g.play_turn(p1, p2)
