from typing import List, Tuple

from state import State, EMPTY_SPACE
from location import Location

#TODO: There is likely a better method for getting candidate translations/moves, but this will do for now

KNIGHT_TRANSLATIONS = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
KING_TRANSLATIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
BISHOP_TRANSLATIONS = [
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), # Northeast diagonal
    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), # Southeast diagonal
    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), # Southwest diagonal
    (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), # Northwest diagonal
]
ROOK_TRANSLATIONS = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), # North
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), # East
    (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), # South
    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), # West
]

class LegalMoveController:
    def __init__(self):
        self.version: str = "0.0.1"

    def getLocationsFromTranslations(self, start: Location, translations: List[Tuple]) -> List[Location]:
        moves = []
        for x, y in translations:
            move = start.translate(x, y)
            if move is None: continue
            moves.append(move)
        return moves

    def is_king_in_check(self, state: State, player: str) -> bool:
        is_white = player == "w"
        king = "K" if is_white else "k" # Which king are we looking at?
        king_locations = state.get_piece_locations(king)
        if len(king_locations) == 0: return False

        king_location = king_locations[0]

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
                new_king_location = king_location.translate(x * scale, y * scale)
                if new_king_location is None:
                    to_remove.append(i)
                    continue
                piece = state.get_piece(new_king_location)
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
                    elif piece.lower() != 'p': # This may be redundant, but just to be safe :)
                        to_remove.append(i)
                        continue
                    else: # Handle pawns
                        if (abs(x) - abs(y)) != 0: # Is not a diagonal direction?
                            to_remove.append(i)
                            continue
                        # Look for black pawns in forward direction
                        if is_white and y > 0: return True
                        # Look for white pawns in backward direction
                        elif is_white and y < 0: return True
            # Remove directions that no longer need to be analyzed
            for idx in reversed(to_remove):
                directions.pop(idx)

        return False

    
    def get_legal_moves(self, state: State, location: Location) -> List[Location]:
        piece = state.get_piece(location)
        # Handle empty location
        if piece == " ": return []

        # Handle invalid turn
        if state.active == "w" and piece.islower(): return []
        if state.active == "b" and piece.isupper(): return []

        if piece.lower() == "n":
            return self.get_legal_knight_moves(state, location)
        if piece.lower() == "k":
            return self.get_legal_king_moves(state, location)
        if piece.lower() == "b":
            return self.get_legal_bishop_moves(state, location)
        if piece.lower() == "r":
            return self.get_legal_rook_moves(state, location)
        if piece.lower() == "q":
            return self.get_legal_queen_moves(state, location)
        if piece.lower() == "p":
            return self.get_legal_pawn_moves(state, location)
        
        return []

    def filter_capture_own_piece_moves(self, state: State, cur_loc: Location, moves: List[Location]) -> List[Location]:
        is_white = state.get_piece(cur_loc).isupper()
        to_remove = []
        for i, m in enumerate(moves):
            is_piece_white = state.get_piece(m).isupper()
            if is_white == is_piece_white:
                to_remove.append(i)
        
        for idx in reversed(to_remove):
            moves.pop(idx)

        return moves

    #? Should I also do an early return if trying to move a piece that isn't the active player's turn??
    def filter_own_king_in_check(self, state: State, loc: Location, moves: List[Location]) -> List[Location]:
        to_remove = []
        piece = state.get_piece(loc)
        for i, m in enumerate(moves):
            new_state = state.copy()
            new_state.position[loc.row][loc.col] = EMPTY_SPACE
            new_state.position[m.row][m.col] = piece
            if self.is_king_in_check(new_state, state.active):
                to_remove.append(i)

        for idx in reversed(to_remove):
            moves.pop(idx)
        
        return moves

    def get_legal_knight_moves(self, state: State, location: Location) -> List[Location]:
        moves = self.getLocationsFromTranslations(location, KNIGHT_TRANSLATIONS)
        moves = self.filter_capture_own_piece_moves(state, location, moves)
        moves = self.filter_own_king_in_check(state, location, moves)
        return moves

    def get_castling_moves(self, state: State) -> List[Location]:
        is_white = state.active == 'w'
        king = 'K' if is_white else 'k'
        valid_options = []
        for opt in state.castling:
            if is_white and opt.isupper():
                valid_options.append(opt.lower())
            elif not is_white and opt.islower():
                valid_options.append(opt)
        if len(valid_options) == 0: return []
        locs = state.get_piece_locations(king)
        if len(locs) == 0: return []
        king_location = locs[0]
        moves = []
        if 'k' in valid_options:
            if state.get_piece(king_location.translate(1, 0)) == EMPTY_SPACE:
                can_loc = king_location.translate(2, 0)
                if state.get_piece(can_loc) == EMPTY_SPACE:
                    moves.append(can_loc)
        if 'q' in valid_options:
            if state.get_piece(king_location.translate(-1, 0)) == EMPTY_SPACE:
                if state.get_piece(king_location.translate(-2, 0)) == EMPTY_SPACE:
                    can_loc = king_location.translate(-3, 0)
                    if state.get_piece(can_loc) == EMPTY_SPACE:
                        moves.append(can_loc)

        return moves

    def get_legal_king_moves(self, state: State, location: Location) -> List[Location]:
        moves = self.getLocationsFromTranslations(location, KING_TRANSLATIONS)
        moves.extend(self.get_castling_moves(state))
        moves = self.filter_capture_own_piece_moves(state, location, moves)
        moves = self.filter_own_king_in_check(state, location, moves)
        return moves

    def get_legal_bishop_moves(self, state: State, location: Location) -> List[Location]:
        moves = self.getLocationsFromTranslations(location, BISHOP_TRANSLATIONS)
        moves = self.filter_capture_own_piece_moves(state, location, moves)
        moves = self.filter_own_king_in_check(state, location, moves)
        return moves
    
    def get_legal_rook_moves(self, state: State, location: Location) -> List[Location]:
        moves = self.getLocationsFromTranslations(location, ROOK_TRANSLATIONS)
        moves = self.filter_capture_own_piece_moves(state, location, moves)
        moves = self.filter_own_king_in_check(state, location, moves)
        return moves
    
    def get_legal_queen_moves(self, state: State, location: Location) -> List[Location]:
        b_moves = self.getLocationsFromTranslations(location, BISHOP_TRANSLATIONS)
        r_moves = self.getLocationsFromTranslations(location, BISHOP_TRANSLATIONS)
        moves = b_moves + r_moves
        assert len(moves) == len(set(b_moves).union(set(r_moves))), "Combined Bishop & Rook moves should not overlap"
        moves = self.filter_capture_own_piece_moves(state, location, moves)
        moves = self.filter_own_king_in_check(state, location, moves)
        return moves

    #TODO is there a cleaner more efficient way to do this?
    def get_legal_pawn_moves(self, state: State, loc: Location) -> List[Location]:
        pawn = state.get_piece[loc]
        if pawn == EMPTY_SPACE: return []
        is_white = pawn.isupper()
        moves = []
        # Get forward moves
        direction = 1 if is_white else -1
        can_move = state.get_piece(loc.translate(0, direction))
        if can_move == EMPTY_SPACE:
            moves.append(can_move)
            can_move = state.get_piece(loc.translate(0, direction.y * 2))
            if can_move == EMPTY_SPACE:
                moves.append(can_move)

        # Look for captures
        can_loc = loc.translate(1, direction.y)
        if can_loc is not None:
            can_piece = state.get_piece(can_loc)
            if can_piece == EMPTY_SPACE:
                if can_loc.notation == state.en_passant:
                    moves.append(can_loc)
            else:
                can_is_white = can_piece.isupper()
                if is_white != can_is_white:
                    moves.append(can_loc)

        can_loc = loc.translate(-1, direction.y)
        if can_loc is not None:
            can_piece = state.get_piece(can_loc)
            if can_piece == EMPTY_SPACE:
                if can_loc.notation == state.en_passant:
                    moves.append(can_loc)
            else:
                can_is_white = can_piece.isupper()
                if is_white != can_is_white:
                    moves.append(can_loc)

        return moves

        

        
        
