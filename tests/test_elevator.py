import pytest
from liftman import Elevator, Passenger


class TestElevator:
    @pytest.fixture()
    def elevator_class_initializer(self):
        basic_elevator = Elevator()
        return basic_elevator

    @pytest.fixture()
    def passengers(self):
        return [Passenger(3, 5), Passenger(4, 8), Passenger(0, 10)]

    def test_elevator_initialization(self):
        elevator = Elevator()
        assert elevator.direction.value == elevator.cur_position == elevator.next_stop == elevator.final_stop == 0
        assert isinstance(elevator.stops, list)
        assert not len(elevator.stops)
