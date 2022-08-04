from typing import List

from state import State
from location import Location

class Engine:
    def __init__(self):
        self.version: str = "0.0.1"
    
    def get_legal_moves(state: State, piece_location: Location) -> List[Location]:
        pass