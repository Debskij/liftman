from typing import List
from liftman import Elevator, Direction, Passenger


def find_closest(proper_elevators: List[Elevator], pos: int) -> Elevator:
    return min(proper_elevators, key=lambda elevator: abs(elevator.cur_position - pos))


class ElevatorOperator:
    def __init__(self, number_of_elevators: int):
        if number_of_elevators < 1:
            raise ValueError
        self.elevators = [Elevator() for _ in range(number_of_elevators)]
        self.waiting_list: List[Passenger] = []

    def step(self) -> bool:
        travel_dist = {elevator.distance_to_stop() for elevator in self.elevators if elevator.distance_to_stop() != 0}
        try:
            travel_dist = min(travel_dist)
        except ValueError:
            return False
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
        return True

    def find_which_elevators(self, passenger: Passenger) -> List[Elevator]:
        return [
            elevator
            for elevator in self.elevators
            if min(elevator.cur_position, elevator.final_stop)
            <= passenger.position
            <= max(elevator.cur_position, elevator.final_stop)
            and elevator.direction == passenger.direction()
        ]

    def call(self, passenger: Passenger) -> None:
        if passenger.position == passenger.destination:
            return
        self.waiting_list.append(passenger)

    def assign_elevator(self, passenger):
        pass
