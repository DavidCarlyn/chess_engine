import unittest

from location import Location

class TestLocation(unittest.TestCase):

    def test_initialization(self):
        loc: Location = Location('e4')
        self.assertEqual(loc.notation, 'e4')
        self.assertEqual(loc.col, 4)
        self.assertEqual(loc.row, 3)

        loc: Location = Location((4, 3))
        self.assertEqual(loc.notation, 'e4')
        self.assertEqual(loc.col, 4)
        self.assertEqual(loc.row, 3)

    def test_update(self):
        loc: Location = Location((0, 0))
        loc.update_by_notation('e4')
        self.assertEqual(loc.notation, 'e4')
        self.assertEqual(loc.col, 4)
        self.assertEqual(loc.row, 3)
        
        loc.update_by_col_row((0, 0))
        self.assertEqual(loc.notation, 'a1')
        self.assertEqual(loc.col, 0)
        self.assertEqual(loc.row, 0)

    def test_failure(self):
        with self.assertRaises(BaseException):
            loc: Location = Location((-1, 0))
        with self.assertRaises(BaseException):
            loc: Location = Location((0, -1))
        with self.assertRaises(BaseException):
            loc: Location = Location((8, 0))
        with self.assertRaises(BaseException):
            loc: Location = Location((0, 8))
        with self.assertRaises(BaseException):
            loc: Location = Location('a0')
        with self.assertRaises(BaseException):
            loc: Location = Location('a9')
        with self.assertRaises(BaseException):
            loc: Location = Location('30')
        with self.assertRaises(BaseException):
            loc: Location = Location('i0')

    def test_bounds(self):
        # Should not raise exceptions
        loc: Location = Location((0, 7))
        loc.update_by_col_row((7, 0))
        loc.update_by_notation('a1')
        loc.update_by_notation('h8')


if __name__ == '__main__':
    unittest.main()