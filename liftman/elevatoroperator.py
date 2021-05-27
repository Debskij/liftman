from typing import List, Optional
from liftman import Elevator, Direction, Passenger


def find_closest(proper_elevators: List[Elevator], pos: int) -> Elevator:
    return min(proper_elevators, key=lambda elevator: abs(elevator.cur_position - pos))


def find_closest_elevator(elevators: List[Elevator], passenger: Passenger) -> Elevator:
    return min(elevators, key=lambda elevator: elevator.distance_to_passenger(passenger))


class ElevatorOperator:
    def __init__(self, number_of_elevators: int):
        if number_of_elevators < 1:
            raise ValueError
        self.elevators = [Elevator() for _ in range(number_of_elevators)]
        self.waiting_list: List[Passenger] = []

    def step(self) -> bool:
        self.resolve_queue()
        try:
            travel_dist = min(
                [elevator.distance_to_stop() for elevator in self.elevators if elevator.distance_to_stop() > 0]
            )
        except ValueError:
            return False
        for elevator in self.elevators:
            if elevator.next_stop != elevator.cur_position:
                elevator.modify_position(travel_dist * elevator.direction.value)
                if elevator.cur_position == elevator.next_stop:
                    if elevator.stops:
                        next_stop = min(elevator.stops, key=lambda stop: abs(elevator.cur_position - stop.position))
                        elevator.set_next_destination(next_stop)
                        elevator.remove_stops(elevator.next_stop)
                    else:
                        elevator.modify_direction(Direction.STAY)
        return True

    def find_passing_elevators(self, passenger: Passenger) -> List[Elevator]:
        return [
            elevator
            for elevator in self.elevators
            if min(elevator.cur_position, elevator.final_stop)
            <= passenger.position
            <= max(elevator.cur_position, elevator.final_stop)
            and elevator.direction == passenger.direction()
        ]

    def idle_elevators(self) -> List[Elevator]:
        return [elevator for elevator in self.elevators if elevator.direction == Direction.STAY]

    def call(self, passenger: Passenger) -> None:
        if passenger.position == passenger.destination:
            return
        self.waiting_list.append(passenger)

    def find_elevator(self, passenger) -> Optional[Elevator]:
        elevators_going_by = self.find_passing_elevators(passenger)
        idle_elevators = self.idle_elevators()
        closest_elevator = None
        if elevators_going_by:
            closest_elevator = find_closest_elevator(elevators_going_by, passenger)
        elif closest_elevator:
            closest_elevator = find_closest_elevator(idle_elevators, passenger)
        return closest_elevator

    def resolve_queue(self):
        passengers_assigned = list()
        for idx, passenger in enumerate(self.waiting_list):
            maybe_elevator = self.find_elevator(passenger)
            if maybe_elevator:
                maybe_elevator += passenger
                passengers_assigned.append(idx)
        self.waiting_list = [
            passenger for idx, passenger in enumerate(self.waiting_list) if idx not in passengers_assigned
        ]
