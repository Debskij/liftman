from enum import Enum
from dataclasses import dataclass


@dataclass
class Passenger:
    id: int
    position: int
    direction: int

    def __str__(self):
        return f"Passenger {self.id}, going from {self.position} to {self.direction}\n"


class Direction(Enum):
    UP = 1
    DOWN = -1
    STAY = 0

    def __int__(self):
        return repr(self)
