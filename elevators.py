from dataclasses import dataclass
from typing import List
from bisect import insort_right


@dataclass
class elevator_dc:
    cur_position: int
    cur_direction: int
    stops: List[int]


class elevator:
    def __init__(self):
        self.cur_position = 0
        self.cur_direction = 0
        self.stops = []

    def __str__(self):
        return f'pos: {self.cur_position}\n' \
               f'dir: {self.cur_direction}\n' \
               f'stops: {self.stops}'

class ElevatorOperator:
    def __init__(self, numberOfElevators: int):
        if numberOfElevators < 1:
            raise ValueError
        self.elevators = numberOfElevators
        self.next_stop = [0 for _ in range(numberOfElevators)]
        self.final_stop = [0 for _ in range(numberOfElevators)]
        self.positions = [0 for _ in range(numberOfElevators)]
        self.stops = [list() for _ in range(numberOfElevators)]
        self.vector = [0 for _ in range(numberOfElevators)]
        self.waiting_list = []

    def step(self):
        travel_dist = {abs(self.next_stop[idx] - self.positions[idx]) for idx in range(self.elevators)}
        try:
            travel_dist.remove(0)
        except KeyError:
            pass
        travel_dist = min(travel_dist)
        for idx in range(self.elevators):
            if self.next_stop[idx] != self.positions[idx]:
                self.positions[idx] += travel_dist * self.vector
                if self.positions[idx] == self.next_stop[idx]:
                    if len(self.stops[idx]):
                        distances = [(in_idx, abs(self.positions[idx] - self.stops[idx][in_idx]))
                                     for in_idx in range(len(self.stops[idx]))]
                        in_idx, _ = min(distances, key=lambda x: x[1])
                        self.next_stop[idx] = self.stops[idx][in_idx]
                        self.stops[idx] = list(filter(lambda x: x != self.stops[idx][in_idx], self.stops[idx]))
                    else:
                        self.vector[idx] = 0

    def find_which_elevators(self, pos: int, dir: int) -> List[int]:
        vector = 1 if pos-dir > 0 else -1
        return [idx for idx in range(self.elevators) if
                min(self.positions[idx], self.final_stop[idx]) <= pos <= max(self.positions[idx], self.final_stop[idx])
                and self.vector == vector]

    def find_closest(self, indexes: List[int], pos: int) -> int:
        return min(indexes, key=lambda x: abs(self.positions[x] - pos))

    def call(self, pos: int, dir: int):
        pass

if __name__ == '__main__':
    e = ElevatorOperator(3)
