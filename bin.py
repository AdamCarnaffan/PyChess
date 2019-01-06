import enum as e

class Argument:
    def __init__(self):
        pass

# Space Types #
###############

class Space(e.Enum):
    Taken = 0
    Enemy = 1
    Available = 2

spaceSprites = {
    Space.Available : "space-available.png",
    Space.Enemy : "space-enemy.png",
    Space.Taken : "space-taken.png"
}