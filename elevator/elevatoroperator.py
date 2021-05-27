from typing import List
from elevator import Elevator
from direction import Direction


class ElevatorOperator:
    def __init__(self, number_of_elevators: int):
        if number_of_elevators < 1:
            raise ValueError
        self.elevators = [Elevator() for _ in range(number_of_elevators)]
        self.waiting_list: List[List[int]] = []

    def step(self):
        travel_dist = {abs(elevator.next_stop - elevator.cur_position) for elevator in self.elevators}
        try:
            travel_dist.remove(0)
        except KeyError:
            pass
        travel_dist = min(travel_dist)
        for elevator in self.elevators:
            if elevator.next_stop != elevator.cur_position:
                elevator.cur_position += travel_dist * elevator.direction.value
                if elevator.cur_position == elevator.next_stop:
                    if len(elevator.stops):
                        distances = [
                            (in_idx, abs(elevator.cur_position - elevator.stops[in_idx]))
                            for in_idx in range(len(elevator.stops))
                        ]
                        in_idx, _ = min(distances, key=lambda x: x[1])
                        elevator.next_stop = elevator.stops[in_idx]
                        elevator.stops = list(filter(lambda x: x != elevator.stops[in_idx], elevator.stops))
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

    def find_closest(self, indexes: List[int], pos: int) -> int:
        return min(indexes, key=lambda x: abs(self.elevators[x].cur_position - pos))

    def call(self, pos: int, destination: int):
        pass


if __name__ == "__main__":
    e = ElevatorOperator(3)
