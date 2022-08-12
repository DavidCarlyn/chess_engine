import unittest
from typing import List

from tests.test_legal_moves import TestLegalMoves
from engine import Engine
from state import State
from location import Location

class TestKingLegalMoves(TestLegalMoves):

    def test_solo_king(self):
        pass

    def test_normal_king_positions(self):
        pass

    def test_castling(self):
        pass

    def test_move_into_check(self):
        pass

    def test_blocks(self):
        pass

    def test_captures(self):
        pass


if __name__ == '__main__':
    unittest.main()