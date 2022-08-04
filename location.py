from typing import Tuple, Union

from cv2 import exp

class Location:
    def __init__(self, loc: Union[Tuple[int, int], str]) -> None:
        self.notation: str
        self.col: int
        self.row: int
        if isinstance(loc, str):
            self.update_by_notation(loc)
        else:
            self.update_by_col_row(loc)

    def update_by_notation(self, value: str):
        self.notation = value
        self.col = ord(value[0]) - ord('a')
        self.row = int(value[1])-1
        if not (self.col >= 0 and self.col < 8):
            raise Exception("Column character must be between a and h")
        if not (self.row >= 0 and self.row < 8):
            raise Exception("Row character must be between 1 and 8")

    def update_by_col_row(self, col_row: Tuple[int, int]) -> None:
        self.col = col_row[0]
        self.row = col_row[1]
        self.notation = chr(ord('a')+self.col) + str(self.row+1)
        if not (self.col >= 0 and self.col < 8):
            raise Exception("Column must be between 0 and 7")
        if not (self.row >= 0 and self.row < 8):
            raise Exception("Row must be between 0 and 7")