from typing import List
from liftman import Direction, Passenger


class Elevator:
    def __init__(self):
        self.cur_position: int = 0
        self.next_stop: int = 0
        self.final_stop: int = 0
        self.going_to_pickup: bool = False
        self.direction: Direction = Direction.STAY
        self.stops: List[Passenger] = []

    def __str__(self):
        return (
            f"pos: {self.cur_position} next stop: {self.next_stop} \n"
            f"final stop: {self.final_stop} direction: {self.direction.name} \n"
            f"stops: {self.stops}"
        )

    def __add__(self, other: Passenger):
        if self.direction == Direction.STAY:
            if self.cur_position == other.position:
                other.taken = True
                self.direction = other.direction()
                self.final_stop = other.destination
                self.next_stop = other.destination
                self.going_to_pickup = False
            else:
                self.direction = self.calculate_direction(other.position)
                self.next_stop = other.position
                self.final_stop = other.destination
                self.going_to_pickup = True
        else:
            if self.going_to_pickup:
                self.final_stop = max(self.final_stop * self.direction.value, other.destination * self.direction.value)
            self.next_stop = min(self.next_stop * self.direction.value, other.destination * self.direction.value)
        self.stops.append(other)
        return self

    def calculate_direction(self, destination: int) -> Direction:
        assert isinstance(destination, int)
        if self.cur_position == destination:
            return Direction.STAY
        return Direction.UP if destination - self.cur_position > 0 else Direction.DOWN

    def distance_to_stop(self) -> int:
        return abs(self.cur_position - self.next_stop)

    def distance_to_passenger(self, passenger: Passenger) -> int:
        assert isinstance(passenger, Passenger)
        return abs(self.cur_position - passenger.position)

    def modify_position(self, new_position: int) -> None:
        assert isinstance(new_position, int)
        self.cur_position = new_position

    def modify_direction(self, new_direction: Direction) -> None:
        assert isinstance(new_direction, Direction)
        self.direction = new_direction

    def remove_stops(self, floor_to_filter: int) -> None:
        assert isinstance(floor_to_filter, int)
        self.stops = list(filter(lambda passenger: passenger.destination != floor_to_filter, self.stops))
        if not self.stops:
            self.direction = Direction.STAY

    def set_next_stop(self, stop: int) -> None:
        assert isinstance(stop, int)
        self.next_stop = stop

    def set_taken_status(self, floor: int) -> None:
        assert isinstance(floor, int)
        for idx, passenger in enumerate(self.stops):
            if passenger.position == floor:
                self.stops[idx].taken = True
