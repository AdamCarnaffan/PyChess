from pieces import *
from chess_class import *
from bin import Argument, Space
from tkinter import Tk, Canvas, PhotoImage

class UI:
    def __init__(self, master, gameController):
        self.master = master
        self.master.title("Chess")
        self.master.geometry('{}x{}'.format(560,560))
        self.canv = Canvas(master, width=560, height=560)
        self.canv.focus_set()
        self.canv.tag_bind("possibility", "<Button-1>", gameController.commit_move)
        self.canv.tag_bind("piece", "<Button-1>", gameController.show_moves)
        self.canv.bind("z", gameController.undo_move)
        self.canv.pack()
        self.draw_board()
        self.draw_pieces(gameController.pieces)

    def draw_board(self):
        for r in range(0,8,1):
            for c in range(r % 2,8,2):
                self.canv.create_rectangle(r*70, c*70, r*70 + 70, c*70 + 70, fill="grey")
        return True

    def draw_possibilities(self, poss):
        self.canv.delete("possibility")
        for p in poss:
            px = p[0] - 1
            py = p[1] - 1
            if len(p) > 2:
                self.canv.create_rectangle(px*70, py*70, px*70 + 70, py*70 + 70, fill="red", stipple='gray50', tags="possibility")
            else:
                self.canv.create_rectangle(px*70, py*70, px*70 + 70, py*70 + 70, fill="orange", stipple='gray50', tags="possibility")
        return True

    def get_coords(self, id):
        return self.canv.coords(id)

    def end_game(self):
        self.canv.create_rectangle(0, 0, 560, 560, fill="red")
        return True

    def clear_draws(self):
        self.canv.delete("piece")
        self.canv.delete("piece-text")
        self.canv.delete("possibility")
        return True

    def draw_pieces(self, pieces):
        self.clear_draws()
        for p in pieces:
            xPos = p.x - 1
            yPos = p.y - 1
            p.set_id(self.canv.create_image(xPos*70 + 35, yPos*70 + 35, image=p.sprite, tags="piece"))
        return True

class Game:
    def __init__(self):
        self.pieces = []
        self.selected = None
        self.playing = 1
        self.playerInCheck = False
        self.backups = []
        self.nextID = 1

    def play(self):
        root = Tk()
        # Build game sprites
        for p in self.pieces:
            p.craft_sprite()
        self.display = UI(root, self)
        root.mainloop()
        return True

    def make_backup(self):
        backup = Game()
        for p in self.pieces:
            backup.pieces = backup.pieces + [p.duplicate()]
        backup.display = self.display
        backup.playing = self.playing
        backup.playerInCheck = self.playerInCheck
        backup.selected = self.selected
        backup.nextID = self.nextID
        backup.backups = list(self.backups)
        self.backups = self.backups + [backup]
        return True

    def assign_id(self):
        self.nextID = self.nextID + 1
        return self.nextID - 1

    def restore_from_backup(self):
        if len(self.backups) < 1:
            return False
        backup = self.backups[len(self.backups) - 1]
        self.pieces = []
        for p in backup.pieces:
            self.pieces = self.pieces + [p]
        self.display = backup.display
        self.playing = backup.playing
        self.selected = backup.selected
        self.nextID = backup.nextID
        self.playerInCheck = backup.playerInCheck
        self.backups = list(backup.backups)
        return True

    def undo_move(self, event = None):
        self.restore_from_backup()
        self.display.draw_pieces(self.pieces)
        return True

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
                path = path + [[initial[0] + direction[0]*v, initial[1] + direction[1]*v]]
        return path

    def check_player_in_check(self, player):
        self.playerInCheck = False
        targ = None
        for p in self.pieces:
            if p.player == player and p.type == Pieces.King:
                targ = p
                break
        if targ is None:
            return False
        for p in self.pieces:
            if p.player != player:
                poss = self.generate_possibilities(p)
                for v in poss:
                    if v[0] == targ.x and v[1] == targ.y:
                        self.playerInCheck = True
                        return True
        return False

    def check_checkmate(self, player):
        for p in self.pieces:
            if p.player == player and len(self.generate_possibilities(p, True)) > 0:
                return False
        return True

    def take_piece(self, pos):
        i = 0
        for p in self.pieces:
            if p.x == pos[0] and p.y == pos[1]:
                self.pieces = self.pieces[0:i] + self.pieces[i+1:len(self.pieces)]
                return True
            i = i + 1
        return False

    def change_turn(self):
        self.change_player()
        self.check_player_in_check(self.playing)
        if self.playerInCheck:
            if self.check_checkmate(self.playing):
                self.display.end_game()
                print("GAME OVER")
                return False
        # AI would make turn here
        # Then turn returns to original player
        return True

    def change_player(self):
        self.playing = 1 if self.playing == 2 else 2
        return True

    def commit_move(self, event):
        pos = self.display.get_coords(event.widget.find_closest(event.x, event.y)[0])
        moveX = int((pos[0])/70 + 1)
        moveY = int((pos[1])/70 + 1)
        piece = self.get_piece_by_uid(self.selected)
        result = self.make_move([moveX, moveY], piece)
        self.display.draw_pieces(self.pieces)
        return result

    def simulate_safe_move(self, pos, piece):
        playing = self.playing
        original = piece.duplicate()
        self.make_move(pos, self.get_piece_by_uid(piece.uid), False) # Backup is made
        safe = True
        if self.check_player_in_check(self.playing):
            safe = False
        self.undo_move()
        piece.restore(original)
        return safe

    def make_move(self, pos, piece, real = True):
        space = self.check_pos_available(pos, piece.player)
        if space == Space.Taken:
            return False
        if piece.type == Pieces.King:
            castle = self.check_castle(self.playing)
        else:
            castle = []
        pieceArgs = piece.get_args(space, castle)
        if piece.move(pos, [piece.x, piece.y], pieceArgs) and not self.check_collision(pos, piece):
            self.make_backup()
            # Check Status of space
            if space == Space.Enemy:
                self.take_piece(pos)
            # Calculate rook movement on castle
            if piece.type == Pieces.King:
                diff = piece.x - pos[0]
                if abs(diff) == 2:
                    if diff < 0:
                        rookPos = [8, piece.y]
                        rookFinal = [6, piece.y]
                    else:
                        rookPos = [1, piece.y]
                        rookFinal = [4, piece.y]
                    rook = self.get_piece_by_pos(rookPos)
                    if rook == False or rook.type != Pieces.Rook:
                        return False
                    rook.complete_move(rookFinal)
            # Begin moving piece
            piece.complete_move(pos)
            
            if real:
                self.change_turn()
            return True
        else:
            return False

    def check_pos_available(self, pos, player):
        for p in self.pieces:
            if p.x == pos[0] and p.y == pos[1]:
                if p.player == player:
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

    def check_castle(self, player):
        possible = []
        for p in self.pieces:
            if p.player == player:
                if p.type == Pieces.King:
                    if p.hasMoved:
                        return []
                    else:
                        king = p
                if p.type == Pieces.Rook:
                    if not p.hasMoved:
                        possible = possible + [p]
        result = []
        other = 2 if player == 1 else 1
        for p in possible:
            # Check empty path
            if self.check_collision([king.x, king.y], p):
                continue
            # Check challenge on squares
            points = self.get_path_points([king.x, king.y], [p.x, p.y])
            for v in self.pieces:
                if v.player == other:
                    poi = self.generate_possibilities(v)
                    for i in points:
                        for l in poi:
                            if l == i:
                                continue
            result = result + [[p.x, p.y]]
        return result

    def generate_possibilities(self, piece, safe = False):
        possibilities = []
        for x in range(1,9,1):
            for y in range(1,9,1):
                space = self.check_pos_available([x,y], piece.player)
                if space == Space.Taken:
                    continue
                if safe and piece.type == Pieces.King:
                    castle = self.check_castle(self.playing)
                else:
                    castle = []
                if piece.move([x,y], [piece.x, piece.y], piece.get_args(space, castle)) and not self.check_collision([x,y], piece):
                    poss = [x,y]
                    #print(poss)
                    if space == Space.Enemy:
                        poss = poss + [1]
                    if safe: # Check that move saves from check
                        if not self.simulate_safe_move(poss, piece):
                            continue
                    possibilities = possibilities + [poss]
        return possibilities
        

    def show_moves(self, event):
        targ = self.get_piece_by_id(event.widget.find_closest(event.x, event.y)[0])
        if targ is False:
            return False
        if targ.player != self.playing:
            return False
        self.selected = targ.uid
        possibilities = self.generate_possibilities(targ, True)
        self.display.draw_possibilities(possibilities)
        return True

    def get_piece_by_id(self, id):
        for p in self.pieces:
            if p.id == id:
                return p
        return False

    def get_piece_by_uid(self, id):
        for p in self.pieces:
            if p.uid == id:
                return p
        return False

    def get_piece_by_pos(self, pos):
        for p in self.pieces:
            if p.x == pos[0] and p.y == pos[1]:
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
            pawnRow = 2 if player == 2 else 7
            mainRow = 1 if player == 2 else 8
            # Add Pawns
            for c in range(1,9,1):
                self.add_piece(Piece(Pieces.Pawn, [c, pawnRow], player, self.assign_id(), 1 if player == 1 else -1))
            # Add Rooks
            self.add_piece(Piece(Pieces.Rook, [1, mainRow], player, self.assign_id())) 
            self.add_piece(Piece(Pieces.Rook, [8, mainRow], player, self.assign_id()))
            # Add Knights
            self.add_piece(Piece(Pieces.Knight, [2, mainRow], player, self.assign_id())) 
            self.add_piece(Piece(Pieces.Knight, [7, mainRow], player, self.assign_id()))
            # Add Bishops
            self.add_piece(Piece(Pieces.Bishop, [3, mainRow], player, self.assign_id()))  
            self.add_piece(Piece(Pieces.Bishop, [6, mainRow], player, self.assign_id()))
            # Add Queen
            self.add_piece(Piece(Pieces.Queen, [4, mainRow], player, self.assign_id()))
            # Add King
            self.add_piece(Piece(Pieces.King, [5, mainRow], player, self.assign_id()))
        return True

def main():
    game = Game()
    game.generate_starting_board()
    game.play()
    return True

main()