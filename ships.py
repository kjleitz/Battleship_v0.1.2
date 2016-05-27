class Ship:
    def __init__(self, name):
        self.name = name
        namedict = {"Aircraft Carrier": 5,
                    "Battleship": 4,
                    "Submarine": 3,
                    "Destroyer": 3,
                    "Patrol Boat": 2,}
        if self.name not in namedict:
            # pass
            raise ValueError("Ship has invalid name. Choose between " +
            "'Aircraft Carrier', 'Battleship', 'Submarine', 'Destroyer', " +
            "and 'Patrol Boat'.")
        self.length = namedict[self.name]
        self.damage = 0
        self.alive = True
        self.coords = []

    def hit(self, x, y):
        self.damage += 1
        self.coords.remove((x, y))
        if self.damage == self.length:
            self.alive = False

    def get_hull_remaining(self):
        return self.length - self.damage


class Buoy:
    def __init__(self):
        self.name = "Buoy"
        self.length = 1


if __name__ == "__main__":
    ship1 = Ship("Battleship")
    print("Ship selected: {}".format(ship1.name))
    for i in ship1.namedict:
        print(i)
