from typing import List

from state import State
from location import Location
from legal_move_controller import LegalMoveController

class Engine:
    def __init__(self):
        self.version: str = "0.0.1"
        self.legal_move_controller: LegalMoveController = LegalMoveController()
    
    def get_legal_moves(self, state: State, location: Location) -> List[Location]:
        return self.legal_move_controller.get_legal_moves(state, location)
