from curses.ascii import isupper
from typing import List, Tuple

from state import State, EMPTY_SPACE
from location import Location

KNIGHT_TRANSLATIONS = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]

class LegalMoveController:
    def __init__(self):
        self.version: str = "0.0.1"

    def getLocationsFromTranslations(self, start: Location, translations: List[Tuple]) -> List[Location]:
        moves = []
        for x, y in KNIGHT_TRANSLATIONS:
            move = start.translate(x, y)
            if move is None: continue
            moves.append(move)
        return moves

    def isKingInCheck(self, state: State, player: str) -> bool:
        is_white = player == "w"
        king = "K" if is_white else "k" # Which king are we looking at?
        king_location = state.get_piece_locations(king)[0]
        def same_color(piece: str, is_white: bool):
            if piece.isupper() and is_white: return True
            if piece.islower() and not is_white: return True
            return False

        #! Knight checks
        knight_locations = self.getLocationsFromTranslations(king_location, KNIGHT_TRANSLATIONS)
        for loc in knight_locations:
            piece = state.get_piece(loc)
            if piece == EMPTY_SPACE: continue
            if piece.lower() != "n": continue
            if same_color(piece, is_white): continue
            return True #! King is in check from opponent knight

        #! Line checks
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        scale = 0
        while len(directions) > 0:
            scale += 1
            to_remove = []
            for i, (x, y) in enumerate(directions):
                piece = state.get_piece(king_location.translate(x * scale, y * scale))
                if piece == EMPTY_SPACE: continue
                if same_color(piece, is_white):
                    to_remove.append(i)
                    continue
                if abs(x) != abs(y): # Rows & Files
                    if piece.lower() in ['k', 'q', 'r']: return True
                    else:
                        to_remove.append(i)
                    continue
                else: # Diagonals
                    if piece.lower() in ['k', 'q', 'b']: return True
                    if scale > 1:
                        to_remove.append(i)
                        continue
                    else:
                        #TODO: handle pawn checks here
            
            #TODO: handle removal of directions here

                

        

    
    def get_legal_moves(self, state: State, location: Location) -> List[Location]:
        piece = state.get_piece(location)
        # Handle empty location
        if piece == " ": return []

        # Handle invalid turn
        if state.active == "w" and piece.islower(): return []
        if state.active == "b" and piece.isupper(): return []

        if piece.lower() == "n":
            return self.get_legal_knight_moves(state, location)
        
        return []

    def get_legal_knight_moves(self, state: State, location: Location) -> List[Location]:
        moves = self.getLocationsFromTranslations(location, KNIGHT_TRANSLATIONS)
        
