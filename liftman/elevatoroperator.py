from typing import List, Optional
from liftman import Elevator, Direction, Passenger


class ElevatorOperator:
    def __init__(self, number_of_elevators: int):
        if number_of_elevators < 1:
            raise ValueError
        self.elevators = [Elevator() for _ in range(number_of_elevators)]
        self.waiting_list: List[Passenger] = []

    @staticmethod
    def find_closest_elevator(elevators: List[Elevator], passenger: Passenger) -> Elevator:
        return min(elevators, key=lambda elevator: elevator.distance_to_passenger(passenger))

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
                    elevator.remove_stops(elevator.cur_position)
                    elevator.remove_pickup(elevator.cur_position)
                    elevator.set_taken_status(elevator.cur_position)
                    next_stop = elevator.calculate_next_stop()
                    elevator.set_next_stop(next_stop)
        return True

    def find_passing_elevators(self, passenger: Passenger) -> List[Elevator]:
        def elevator_passing_by(elevator: Elevator) -> bool:
            if elevator.direction != passenger.direction():
                return False
            elif (
                elevator.pickup_direction == passenger.direction() and elevator.direction == passenger.direction()
            ) or elevator.pickup_floor is None:
                return position_between_two_values(elevator.cur_position, elevator.final_stop)
            else:
                return position_between_two_values(elevator.cur_position, elevator.pickup_floor)

        def position_between_two_values(first_position: int, second_position: int) -> bool:
            return min(first_position, second_position) <= passenger.position <= max(first_position, second_position)

        return [elevator for elevator in self.elevators if elevator_passing_by(elevator)]

    def idle_elevators(self) -> List[Elevator]:
        return [elevator for elevator in self.elevators if elevator.direction == Direction.STAY]

    def call(self, passenger: Passenger) -> None:
        assert not passenger.position == passenger.destination
        print(f"Added passenger {passenger} to waiting list")
        self.waiting_list.append(passenger)

    def find_elevator(self, passenger) -> Optional[Elevator]:
        elevators_going_by = self.find_passing_elevators(passenger)
        idle_elevators = self.idle_elevators()
        closest_elevator = None
        if elevators_going_by:
            closest_elevator = self.find_closest_elevator(elevators_going_by, passenger)
        elif idle_elevators:
            closest_elevator = self.find_closest_elevator(idle_elevators, passenger)
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
