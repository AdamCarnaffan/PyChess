from pieces import *
from chess_class import *
from bin import Argument, Space
from tkinter import Tk, Button, Canvas, Frame

class UI:
    def __init__(self, master, gameController):
        self.master = master
        self.master.title("Chess")
        self.master.geometry('{}x{}'.format(600,600))

        self.canv = Canvas(master, width=600, height=600)
        self.canv.focus_set()
        self.canv.tag_bind("possibility", "<Button-1>", gameController.make_move)
        self.canv.tag_bind("piece", "<Button-1>", gameController.generate_possibilities)
        self.canv.pack()
        self.draw_board()
        self.draw_pieces(gameController.pieces)

    def draw_board(self):
        for r in range(0,8,1):
            for c in range(r % 2,8,2):
                self.canv.create_rectangle(r*75, c*75, r*75 + 75, c*75 + 75, fill="purple")
        return True

    def draw_possibilities(self, poss):
        self.canv.delete("possibility")
        for p in poss:
            px = p[0] - 1
            py = p[1] - 1
            if len(p) > 2:
                self.canv.create_rectangle(px*75 + 5, py*75 + 5, px*75 + 70, py*75 + 70, fill="red", tags="possibility")
            else:
                self.canv.create_rectangle(px*75 + 5, py*75 + 5, px*75 + 70, py*75 + 70, fill="orange", tags="possibility")
        return True

    def get_coords(self, id):
        return self.canv.coords(id)

    def clear_draws(self):
        self.canv.delete("piece")
        self.canv.delete("piece-text")
        self.canv.delete("possibility")
        return True

    def draw_pieces(self, pieces):
        self.clear_draws()
        for p in pieces:
            color = "green" if p.player == 1 else "blue"
            xPos = p.x - 1
            yPos = p.y - 1
            p.set_id(self.canv.create_rectangle(xPos*75 + 5, yPos*75 + 5, xPos*75 + 70, yPos*75 + 70, fill=color, tags="piece"))
            self.canv.create_text(xPos*75 + 42, yPos*75 + 42, fill="black", text=str(p.type), tags="piece-text")
        return True

class Game:
    def __init__(self):
        root = Tk()
        self.pieces = []
        self.generate_starting_board()
        self.display = UI(root, self)
        self.selected = None
        self.playing = 1
        self.playerInCheck = False
        root.mainloop()

    def get_path_points(self, final, initial):
        if final[0] == initial[0] and final[1] == initial[1]:
            return []
        path = []
        direction = [0, 0]
        direction[0] = int(abs(final[0] - initial[0])/(final[0] - initial[0])) if final[0] - initial[0] != 0 else 0
        direction[1] = int(abs(final[1] - initial[1])/(final[1] - initial[1])) if final[1] - initial[1] != 0 else 0
        if final[0] == initial[0]:
            for v in range(int(initial[1] + direction[1]), int(final[1]), direction[1]):
                path = path + [[final[0], v]]
        elif final[1] == initial[1]:
            for v in range(int(initial[0] + direction[0]), int(final[0]), direction[0]):
                path = path + [[v, final[1]]]
        else:
            if abs(final[0] - initial[0]) != abs(final[1] - initial[1]):
                return []
            for v in range(1, int(abs(final[0] - initial[0])), 1):
                path = path + [[direction[0]*v, direction[1]*v]]
        return path

    def check_player_in_check(self):
        pass

    def take_piece(self, pos):
        pass

    def change_turn(self):
        self.playing = 1 if self.playing == 2 else 2
        self.check_player_in_check()
        return True

    def make_move(self, event):
        pos = self.display.get_coords(event.widget.find_closest(event.x, event.y)[0])
        moveX = (pos[0] - 5)/75 + 1
        moveY = (pos[1] - 5)/75 + 1
        piece = self.selected
        space = self.check_pos_available([moveX, moveY])
        if space == Space.Taken:
            return False
        pieceArgs = piece.get_args(space)
        if self.selected.move([moveX, moveY], [piece.x, piece.y], pieceArgs) and not self.check_collision([moveX, moveY], piece):
            # Check Status of space
            if space == Space.Enemy:
                self.take_piece([moveX, moveY])
            # Begin moving piece
            piece.x = moveX
            piece.y = moveY
            piece.hasMoved = True
            self.change_turn()
            self.display.draw_pieces(self.pieces)
            return True
        else:
            return False

    def check_pos_available(self, pos):
        for p in self.pieces:
            if p.x == pos[0] and p.y == pos[1]:
                if p.player == self.playing:
                    return Space.Taken
                else:
                    return Space.Enemy
        return Space.Available

    def check_collision(self, pos, piece):
        if piece.type == Pieces.Knight:
            return False
        points = self.get_path_points(pos, [piece.x, piece.y])
        for v in points:
            for p in self.pieces:
                if p.x == v[0] and p.y == v[1]:
                    return True
        return False

    def generate_possibilities(self, event):
        targ = self.get_piece_by_id(event.widget.find_closest(event.x, event.y)[0])
        if targ.player != self.playing:
            return False
        self.selected = targ
        possibilities = []
        for x in range(1,9,1):
            for y in range(1,9,1):
                space = self.check_pos_available([x,y])
                if space == Space.Taken:
                    continue
                if targ.move([x,y], [targ.x, targ.y], targ.get_args(space)) and not self.check_collision([x,y], targ):
                    poss = [x,y]
                    if space == Space.Enemy:
                        poss = poss + [1]
                    possibilities = possibilities + [poss]
        self.display.draw_possibilities(possibilities)
        return True

    def get_piece_by_id(self, id):
        for p in self.pieces:
            if p.id == id:
                return p
        return False

    def add_piece(self, piece):
        self.pieces = self.pieces + [piece]
        return True

    def remove_piece(self, target):
        i = 0
        for p in self.pieces:
            if p.id == target:
                self.pieces = self.pieces[0:i] + self.pieces[i+1:len(self.pieces)]
                return True
            i = i + 1
        return False

    def generate_starting_board(self):
        for player in range(1,3,1):
            pawnRow = 2 if player == 1 else 7
            mainRow = 1 if player == 1 else 8
            # Add Pawns
            for c in range(1,9,1):
                self.add_piece(Piece(Pieces.Pawn, [c, pawnRow], player, 1 if player == 2 else -1))
            # Add Rooks
            self.add_piece(Piece(Pieces.Rook, [1, mainRow], player)) 
            self.add_piece(Piece(Pieces.Rook, [8, mainRow], player))
            # Add Knights
            self.add_piece(Piece(Pieces.Knight, [2, mainRow], player)) 
            self.add_piece(Piece(Pieces.Knight, [7, mainRow], player))
            # Add Bishops
            self.add_piece(Piece(Pieces.Bishop, [3, mainRow], player))  
            self.add_piece(Piece(Pieces.Bishop, [6, mainRow], player))
            # Add Queen
            self.add_piece(Piece(Pieces.Queen, [5, mainRow], player))
            # Add King
            self.add_piece(Piece(Pieces.King, [4, mainRow], player))
        return True

def main():
    game = Game()
    return True

main()