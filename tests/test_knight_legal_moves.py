import unittest
from typing import List

from tests.test_legal_moves import TestLegalMoves
from engine import Engine
from state import State
from location import Location

class TestKnightLegalMoves(TestLegalMoves):

    def assertLocationIn(self, loc: Location, locations: List[Location]):
        notations = list(map(lambda x: x.notation, locations))
        self.assertIn(loc.notation, notations)
    
    def assertLocationNotIn(self, loc: Location, locations: List[Location]):
        notations = list(map(lambda x: x.notation, locations))
        self.assertNotIn(loc.notation, notations)

    def test_solo_knight(self):
        state: State = State("8/8/8/4N3/8/8/8/8 w - - 0 1")
        engine: Engine = Engine()
        moves = engine.get_legal_moves(state, Location('e5'))
        self.assertEqual(len(moves), 8)
        self.assertLocationIn(Location('d7'), moves)
        self.assertLocationIn(Location('f7'), moves)
        self.assertLocationIn(Location('c6'), moves)
        self.assertLocationIn(Location('g6'), moves)
        self.assertLocationIn(Location('g4'), moves)
        self.assertLocationIn(Location('c4'), moves)
        self.assertLocationIn(Location('f3'), moves)
        self.assertLocationIn(Location('d3'), moves)

        state.set_state("8/8/8/8/8/8/8/N7 w - - 0 1")
        moves = engine.get_legal_moves(state, Location('a1'))
        self.assertEqual(len(moves), 2)
        self.assertLocationIn(Location('c2'), moves)
        self.assertLocationIn(Location('b3'), moves)
        
        state.set_state("8/8/8/8/8/8/8/N7 w - - 0 1")


if __name__ == '__main__':
    unittest.main()