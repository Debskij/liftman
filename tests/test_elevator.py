import pytest
from liftman import Elevator, Passenger, Direction


# noinspection PyTypeChecker
class TestElevator:
    @pytest.fixture()
    def elevator(self):
        return Elevator()

    def test_elevator_initialization(self, elevator):
        assert elevator.direction.value == elevator.cur_position == elevator.next_stop == elevator.final_stop == 0
        assert isinstance(elevator.stops, list)
        assert not len(elevator.stops)

    def test_string_of_elevator(self, elevator):
        log_print = str(elevator).split(" ")
        assert str(elevator.cur_position) in log_print
        assert str(elevator.next_stop) in log_print
        assert str(elevator.final_stop) in log_print
        assert str(elevator.direction.STAY.name) in log_print

    def test_elevator_add_one_passenger_different_floor(self, elevator):
        new_passenger = Passenger(1, 5)
        elevator += new_passenger
        assert elevator.next_stop == 1
        assert elevator.final_stop == 5
        assert elevator.cur_position == 0
        assert elevator.stops == [new_passenger]
        assert elevator.direction == Direction.UP

    def test_elevator_add_one_passenger_same_floor(self, elevator):
        new_passenger = Passenger(0, 5)
        elevator += new_passenger
        assert elevator.next_stop == 5
        assert elevator.final_stop == 5
        assert elevator.cur_position == 0
        assert elevator.stops == [new_passenger]
        assert elevator.direction == Direction.UP

    def test_step_multiple_passengers(self, elevator):
        passengers = [Passenger(floor, floor + 3) for floor in range(1, 10)]
        for passenger in passengers:
            elevator += passenger
        assert len(elevator.stops) == len(passengers)
        assert elevator.cur_position == 0
        assert elevator.direction == Direction.UP

    def test_direction_calculation(self, elevator):
        assert elevator.calculate_direction(elevator.cur_position + 5) == Direction.UP
        assert elevator.calculate_direction(elevator.cur_position) == Direction.STAY
        assert elevator.calculate_direction(elevator.cur_position - 5) == Direction.DOWN

    def test_distance_to_stop(self, elevator):
        elevator.cur_position = 5
        elevator.next_stop = -5
        assert elevator.distance_to_stop() == 10
        elevator.next_stop = 5
        assert elevator.distance_to_stop() == 0
        elevator.next_stop = 15
        assert elevator.distance_to_stop() == 10

    def test_distance_to_passenger(self, elevator):
        new_passenger = Passenger(1, 5)
        assert elevator.distance_to_passenger(new_passenger) == 1
        with pytest.raises(AssertionError):
            _ = elevator.distance_to_passenger(1)

    def test_modify_position(self, elevator):
        assert elevator.cur_position == 0
        elevator.modify_position(5)
        assert elevator.cur_position == 5
        with pytest.raises(AssertionError):
            elevator.modify_position(3.5)

    def test_modify_direction(self, elevator):
        assert elevator.direction == Direction.STAY
        elevator.modify_direction(Direction.UP)
        assert elevator.direction == Direction.UP
        elevator.modify_direction(Direction.DOWN)
        assert elevator.direction == Direction.DOWN
        with pytest.raises(AssertionError):
            elevator.modify_direction(5)

    def test_remove_stops(self, elevator):
        passengers_list = [
            Passenger(1, 6),
            Passenger(2, 6),
            Passenger(3, 6),
            Passenger(6, 7),
            Passenger(6, 6),
            Passenger(1, 5),
        ]
        for passenger in passengers_list:
            elevator += passenger
        assert elevator.direction == Direction.UP
        assert len(elevator.stops) == len(passengers_list)
        elevator.remove_stops(6)
        assert len(elevator.stops) == 2
        assert not [passenger for passenger in elevator.stops if passenger.destination == 6]
        elevator.remove_stops(7)
        assert len(elevator.stops) == 1
        assert not [
            passenger for passenger in elevator.stops if passenger.destination == 6 or passenger.destination == 7
        ]
        elevator.remove_stops(5)
        assert len(elevator.stops) == 0
        assert elevator.direction == Direction.STAY
        with pytest.raises(AssertionError):
            elevator.remove_stops(2.5)

    def test_set_next_stop(self, elevator):
        assert elevator.next_stop == 0
        elevator.set_next_stop(5)
        assert elevator.next_stop == 5
        with pytest.raises(AssertionError):
            elevator.set_next_stop(2.5)

    def test_set_taken_status(self, elevator):
        passengers_list = [
            Passenger(0, 6),
            Passenger(1, 3),
            Passenger(1, 5),
            Passenger(1, 6),
            Passenger(2, 6),
            Passenger(4, 7),
            Passenger(4, 6),
        ]
        assert len(elevator.stops) == 0
        for passenger in passengers_list:
            elevator += passenger
        assert elevator.stops == passengers_list
        assert [passenger.taken for passenger in elevator.stops].count(True) == 1
        elevator.set_taken_status(1)
        assert [passenger.taken for passenger in elevator.stops].count(True) == 4
        assert len(elevator.stops) == len(passengers_list)
