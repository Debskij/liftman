from typing import List, Type
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

    def __add__(self, other: Passenger):
        if self.direction == Direction.STAY:
            self.direction = other.direction()
        self.stops.append(other)

    def distance_to_stop(self) -> int:
        return abs(self.cur_position - self.next_stop)

    def distance_to_passenger(self, passenger: Passenger) -> int:
        return abs(self.cur_position - passenger.position)

    def modify_position(self, new_position: int) -> None:
        assert isinstance(new_position, int)
        self.cur_position = new_position

    def modify_direction(self, new_direction: Direction) -> None:
        assert isinstance(new_direction, Direction)
        self.direction = new_direction

    def remove_stops(self, floor_to_filter: int) -> None:
        self.stops = list(filter(lambda passenger: passenger.destination != floor_to_filter, self.stops))

    def set_next_destination(self, stop: Passenger):
        self.next_stop = stop.destination
