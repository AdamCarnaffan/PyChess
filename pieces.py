import enum as e

# Piece Definitions #
#####################

class Pieces(e.Enum):
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6

def rook(x, y):
    print(x, y)
    return True

def pawn():
    pass

def bishop():
    pass

def knight():
    pass

def queen():
    pass

def king():
    pass

moves = {
    Pieces.Pawn : pawn,
    Pieces.Rook : rook,
    Pieces.Knight : knight,
    Pieces.Bishop : bishop,
    Pieces.Queen : queen,
    Pieces.King : king
}

# Support Functions #
#####################

def get_movement(type):
    return moves[type]
