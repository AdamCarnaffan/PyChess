from pieces import *
from bin import Argument, Space
from tkinter import PhotoImage

class Piece:
    def __init__(self, type, position, owner, dir = None):
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
        self.craft_sprite()

    def craft_sprite(self):
        playerStr = "wht-" if self.player == 1 else "blk-"
        pieceStr = get_piece_sprite(self.type)
        self.sprite = PhotoImage(file='sprites/{}'.format(playerStr + pieceStr))
        return True

    def get_move_function(self):
        self.move = get_movement(self.type)
        return True

    def get_args(self, spaceStatus):
        args = Argument()
        args.moved = self.hasMoved
        args.spaceContainsEnemy = True if spaceStatus == Space.Enemy else False
        args.direction = self.direction # For Pawn Move Direction
        args.isInCheck = False # Needs to be evaluated
        args.protectingKing = False # Needs to be evaluated
        args.hasLineToKing = False # Needs to be evaluated --> For castling
        return args

    def set_id(self, val):
        self.id = val
        return True
    