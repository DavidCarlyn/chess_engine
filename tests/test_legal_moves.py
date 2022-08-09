import unittest
from typing import List

from location import Location

class TestLegalMoves(unittest.TestCase):

    def assertLocationIn(self, loc: Location, locations: List[Location]):
        notations = list(map(lambda x: x.notation, locations))
        self.assertIn(loc.notation, notations)
    
    def assertLocationNotIn(self, loc: Location, locations: List[Location]):
        notations = list(map(lambda x: x.notation, locations))
        self.assertNotIn(loc.notation, notations)


if __name__ == '__main__':
    unittest.main()