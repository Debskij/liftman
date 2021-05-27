from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1
    STAY = 0

    def __int__(self):
        return repr(self)
