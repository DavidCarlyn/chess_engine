import unittest

from state import State

class TestState(unittest.TestCase):

    def check_row(self, row, str_state):
        for i, space in enumerate(row):
            self.assertEqual(space, str_state[i])

    def test_initialization(self):
        state: State = State()
        self.assertEqual(state.active, "w")
        self.assertEqual(state.castling, "KQkq")
        self.assertEqual(state.en_passant, "-")
        self.assertEqual(state.half_moves, 0)
        self.assertEqual(state.turn, 1)

        self.check_row(state.position[0], "RNBQKBNR")
        self.check_row(state.position[1], "PPPPPPPP")
        self.check_row(state.position[2], "        ")
        self.check_row(state.position[3], "        ")
        self.check_row(state.position[4], "        ")
        self.check_row(state.position[5], "        ")
        self.check_row(state.position[6], "pppppppp")
        self.check_row(state.position[7], "rnbqkbnr")

        self.assertEqual(state.get_fen(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        state = State("r1b1kbnr/pppp1ppp/2n5/8/2BPPp1q/8/PPP3PP/RNBQ1KNR b kq d3 0 5")

        self.assertEqual(state.active, "b")
        self.assertEqual(state.castling, "kq")
        self.assertEqual(state.en_passant, "d3")
        self.assertEqual(state.half_moves, 0)
        self.assertEqual(state.turn, 5)

        self.check_row(state.position[0], "RNBQ KNR")
        self.check_row(state.position[1], "PPP   PP")
        self.check_row(state.position[2], "        ")
        self.check_row(state.position[3], "  BPPp q")
        self.check_row(state.position[4], "        ")
        self.check_row(state.position[5], "  n     ")
        self.check_row(state.position[6], "pppp ppp")
        self.check_row(state.position[7], "r b kbnr")

        self.assertEqual(state.get_fen(), "r1b1kbnr/pppp1ppp/2n5/8/2BPPp1q/8/PPP3PP/RNBQ1KNR b kq d3 0 5")

    def test_failures(self):
        pass

    def test_update(self):
        pass

    def test_bounds(self):
        pass

    def test_get_piece(self):
        pass


if __name__ == '__main__':
    unittest.main()