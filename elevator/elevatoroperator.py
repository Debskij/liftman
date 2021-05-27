from typing import List
from elevator import Elevator
from helpers import Direction, Passenger


def find_closest(proper_elevators: List[Elevator], pos: int) -> Elevator:
    return min(proper_elevators, key=lambda elevator: abs(elevator.cur_position - pos))


class ElevatorOperator:
    def __init__(self, number_of_elevators: int):
        if number_of_elevators < 1:
            raise ValueError
        self.elevators = [Elevator() for _ in range(number_of_elevators)]
        self.waiting_list: List[Passenger] = []

    def step(self):
        travel_dist = {elevator.distance_to_stop() for elevator in self.elevators if elevator.distance_to_stop() != 0}
        travel_dist = min(travel_dist)
        for elevator in self.elevators:
            if elevator.next_stop != elevator.cur_position:
                elevator.cur_position += travel_dist * elevator.direction.value
                if elevator.cur_position == elevator.next_stop:
                    if elevator.stops:
                        distances = [
                            (in_idx, abs(elevator.cur_position - elevator.stops[in_idx].position))
                            for in_idx in range(len(elevator.stops))
                        ]
                        in_idx, _ = min(distances, key=lambda x: x[1])
                        elevator.stops = list(filter(lambda x: x != elevator.next_stop, elevator.stops))
                    else:
                        elevator.direction = Direction.STAY

    def find_which_elevators(self, pos: int, destination: int) -> List[int]:
        direction = Direction.UP if pos - destination > 0 else Direction.DOWN

        return [
            idx
            for idx, elevator in enumerate(self.elevators)
            if min(elevator.cur_position, elevator.final_stop)
            <= pos
            <= max(elevator.cur_position, elevator.final_stop)
            and elevator.direction == direction
        ]

    def call(self, passenger: Passenger):
        self.waiting_list.append(passenger)

    def assign_elevator(self, passenger):
        pass
