from pieces import *

class Piece:
    def __init__(self, type, position):
        self.type = type
        self.x = position[0]
        self.y = position[1]
        self.get_move_function()

    def get_move_function(self):
        self.move = get_movement(self.type)
        return True


