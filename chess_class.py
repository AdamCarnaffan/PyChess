from pieces import *
from bin import Argument, Space
from tkinter import PhotoImage

class Piece:
    def __init__(self, type, position, owner, uid, dir = None):
        self.type = type
        self.x = position[0]
        self.y = position[1]
        self.hasMoved = False
        self.player = owner
        self.direction = 0
        if dir != None:
            self.direction = dir
        self.get_move_function()
        self.id = -1
        self.uid = uid

    def craft_sprite(self):
        playerStr = "wht-" if self.player == 1 else "blk-"
        pieceStr = get_piece_sprite(self.type)
        self.sprite = PhotoImage(file='sprites/{}'.format(playerStr + pieceStr))
        return True

    def get_move_function(self):
        self.move = get_movement(self.type)
        return True

    def get_args(self, spaceStatus, availableCastles):
        args = Argument()
        args.moved = self.hasMoved
        args.spaceContainsEnemy = True if spaceStatus == Space.Enemy else False
        args.direction = self.direction # For Pawn Move Direction
        args.castles = availableCastles
        return args

    def duplicate(self):
        dup = Piece(self.type, [self.x, self.y], self.player, self.uid, self.direction)
        dup.hasMoved = self.hasMoved
        dup.craft_sprite()
        return dup

    def restore(self, backup):
        self.x = backup.x
        self.y = backup.y
        self.uid = backup.uid # should already match
        self.type = backup.type
        self.hasMoved = backup.hasMoved
        self.sprite = backup.sprite
        self.direction = backup.direction
        self.player = backup.player
        return True

    def set_id(self, val):
        self.id = val
        return True

    def complete_move(self, pos):
        self.hasMoved = True
        self.x = int(pos[0])
        self.y = int(pos[1])
        return True
    