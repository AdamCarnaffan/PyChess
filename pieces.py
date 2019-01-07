import enum as e
from bin import Argument

# Helper Functions #
####################

def convertToChar(pos):
    if pos == 1:
        return "A"
    elif pos == 2:
        return "B"
    elif pos == 3:
        return "C"
    elif pos == 4:
        return "D"
    elif pos == 5:
        return "E"
    elif pos == 6:
        return "F"
    elif pos == 7:
        return "G"
    elif pos == 8:
        return "H"
    else:
        ValueError("Invalid Position")

def convertToPos(character):
    if character == "A":
        return 1
    elif character == "B":
        return 2
    elif character == "C":
        return 3
    elif character == "D":
        return 4
    elif character == "E":
        return 5
    elif character == "F":
        return 6
    elif character == "G":
        return 7
    elif character == "H":
        return 8
    else:
        ValueError("Invalid Position Value!")

# Piece Definitions #
#####################

class Pieces(e.Enum):
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6

def validate_position(pos):
    for v in pos:
        if v > 8 or v < 1:
            return False
    return True

# Piece Moves #
###############

def rook(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = abs(oldPos[1] - pos[1])
    if diffx == 0 and diffy != 0:
        return True
    elif diffy == 0 and diffx != 0:
        return True
    return False

def pawn(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = oldPos[1] - pos[1]
    if diffx > 0:
        if take(pos, oldPos, arg):
            return True
        return False
    if arg.spaceContainsEnemy:
        return False
    if diffy == arg.direction:
        return True
    elif diffy == 2*arg.direction and not arg.moved:
        return True
    return False

def bishop(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = abs(oldPos[1] - pos[1])
    if diffx == diffy:
        return True
    return False

def knight(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = abs(oldPos[1] - pos[1])
    if diffx == 2 and diffy == 1:
        return True
    elif diffx == 1 and diffy == 2:
        return True
    return False

def queen(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = abs(oldPos[1] - pos[1])
    if diffx == diffy:
        return True
    elif diffx == 0 and diffy != 0:
        return True
    elif diffy == 0 and diffx != 0:
        return True
    return False

def king(pos, oldPos, arg):
    if not validate_position(pos): # Validate the position input for the move
        return False
    diffx = abs(oldPos[0] - pos[0])
    diffy = abs(oldPos[1] - pos[1])
    if diffx > 1 or diffy > 1:
        if castle(pos, oldPos, arg):
            return True
        return False
    # Needs to not put self into check
    return True

# Special Movements #
#####################

def castle(pos, oldPos, arg):
    if len(arg.castles) <= 0:
        return False
    for p in arg.castles:
        # Direction based on rook x
        diffx = 2 if p[0] > oldPos[0] else -2
        if pos[0] == oldPos[0] + diffx and pos[1] == oldPos[1]:
            return True
    return False

def take(pos, oldPos, arg):
    diffx = abs(oldPos[0] - pos[0])
    diffy = oldPos[1] - pos[1]
    if diffx == 1 and diffy == arg.direction:
        if arg.spaceContainsEnemy:
            return True
    return False

# Piece Tuples #
###############

moves = {
    Pieces.Pawn : pawn,
    Pieces.Rook : rook,
    Pieces.Knight : knight,
    Pieces.Bishop : bishop,
    Pieces.Queen : queen,
    Pieces.King : king
}

sprites = {
    Pieces.Pawn : "pawn.png",
    Pieces.Rook : "rook.png",
    Pieces.Knight : "knight.png",
    Pieces.Bishop : "bishop.png",
    Pieces.Queen : "queen.png",
    Pieces.King : "king.png",
}

# Support Functions #
#####################

def get_movement(type):
    return moves[type]

def get_piece_sprite(type):
    return sprites[type]