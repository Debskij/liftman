from typing import List
from liftman import Direction, Passenger


class Elevator:
    def __init__(self):
        self.cur_position: int = 0
        self.next_stop: int = 0
        self.final_stop: int = 0
        self.direction: Direction = Direction.STAY
        self.stops: List[Passenger] = []

    def __str__(self):
        return (
            f"pos: {self.cur_position} next stop: {self.next_stop}\n"
            f"final stop: {self.final_stop} direction: {Direction.name}\n"
            f"stops: {self.stops}"
        )

    def distance_to_stop(self):
        return abs(self.cur_position - self.next_stop)