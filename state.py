from copy import copy
from typing import List

from location import Location

EMPTY_SPACE = " "
class State:
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.position: List[List[str]]
        self.active: str
        self.castling: str
        self.en_passant: str
        self.half_moves: int
        self.turn: int
        self.set_state(fen)

    def set_state(self, fen: str) -> None:
        try:
            position, active, castling, en_passant, half_moves, turn = fen.split(" ")
        except:
            raise Exception("Invalid FEN. All parts not present")

        rows = position.split("/")
        if len(rows) < 8:
            raise Exception("Invalid FEN. Position must have 8 rows")

        # Setting position
        self.position = [[EMPTY_SPACE] * 8 for _ in range(8)]
        for i, row in enumerate(reversed(rows)):
            j = 0
            for space in row:
                if space.isdigit():
                    j += int(space) - 1
                else:
                    self.position[i][j] = space
                j += 1
            if j < 8:
                raise Exception("Invalid FEN. Each row must have 8 spaces")

        # Setting Position information
        self.active = active
        self.castling = castling
        self.en_passant = en_passant
        self.half_moves = int(half_moves)
        self.turn = int(turn)

    def get_piece(self, location: Location) -> str:
        return self.position[location.row][location.col]

    def get_piece_locations(self, piece: str) -> List[Location]:
        #? Should I just raise an exception here if these cases fail???
        #! Maybe not if we want to allow fun and weird gamemodes.
        if not isinstance(piece, str): return []
        if piece.lower() not in ['p', 'r', 'n', 'b', 'q', 'k']: return []

        locations = []
        for i, row in enumerate(self.position):
            for j, space in enumerate(row):
                if space == piece:
                    locations.append(Location((j, i)))

        return locations

    def get_fen(self):
        position = ""
        for i, row in enumerate(reversed(self.position)):
            counter = 0
            for space in row:
                if space == EMPTY_SPACE:
                    counter += 1
                else: 
                    if counter > 0:
                        position += str(counter)
                        counter = 0
                    position += space
            if counter > 0:
                position += str(counter)
            if i < (len(self.position)-1):
                position += "/"

        fen = f"{position} {self.active} {self.castling} {self.en_passant} {self.half_moves} {self.turn}"
        return fen

    def copy(self):
        return copy(self)


        