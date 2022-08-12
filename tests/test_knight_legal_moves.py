import unittest
from typing import List

from tests.test_legal_moves import TestLegalMoves
from engine import Engine
from state import State
from location import Location

class TestKnightLegalMoves(TestLegalMoves):

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

    def test_normal_knight_positions(self):
        state: State = State("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        engine: Engine = Engine()
        moves = engine.get_legal_moves(state, Location('g1'))
        self.assertEqual(len(moves), 2)
        self.assertLocationIn(Location('f3'), moves)
        self.assertLocationIn(Location('h3'), moves)

        state.set_state("5rk1/1p3ppp/p2B1n2/5bb1/2r5/2N2P2/PPP3PP/1K1R3R w - - 0 18")
        moves = engine.get_legal_moves(state, Location('c3'))
        self.assertEqual(len(moves), 5)
        self.assertLocationIn(Location('e2'), moves)
        self.assertLocationIn(Location('e4'), moves)
        self.assertLocationIn(Location('d5'), moves)
        self.assertLocationIn(Location('b5'), moves)
        self.assertLocationIn(Location('a4'), moves)

    def test_pinned_knight(self):
        state: State = State("8/8/5k2/4b3/3N4/2K5/8/8 w - - 0 1")
        engine: Engine = Engine()
        moves = engine.get_legal_moves(state, Location('d4'))
        self.assertEqual(len(moves), 0)

        state.set_state("8/3k4/3r4/8/3N4/3K4/8/8 w - - 0 1")
        moves = engine.get_legal_moves(state, Location('d4'))
        self.assertEqual(len(moves), 0)

    def test_blocks(self):
        pass

    def test_captures(self):
        pass


if __name__ == '__main__':
    unittest.main()