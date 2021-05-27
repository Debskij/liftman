from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 1
    DOWN = -1
    STAY = 0


@dataclass
class Passenger:
    position: int
    destination: int

    def __str__(self):
        return f"Passenger going from {self.position} to {self.destination}\n"

    def direction(self) -> Direction:
        if self.position == self.destination:
            raise ValueError
        return Direction.UP if self.destination - self.position > 0 else Direction.DOWN

    def amount_of_floors(self) -> int:
        return abs(self.position - self.destination)
