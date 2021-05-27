from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 1
    DOWN = -1
    STAY = 0

    def __int__(self):
        return repr(self)


@dataclass
class Passenger:
    id: int
    position: int
    destination: int

    def __str__(self):
        return f"Passenger {self.id}, going from {self.position} to {self.destination}\n"

    def direction(self) -> Direction:
        return Direction.UP if self.position - self.destination > 0 else Direction.DOWN

    def amount_of_floors(self) -> int:
        return abs(self.position - self.destination)
