import pytest
from liftman import ElevatorOperator, Elevator, Direction, Passenger


class TestElevatorOperator:
    def test_initialization_of_elevator_operator(self):
        elevator_operator = ElevatorOperator(3)
        assert len(elevator_operator.elevators) == 3
        assert len(elevator_operator.waiting_list) == 0
        with pytest.raises(ValueError):
            _ = ElevatorOperator(0)
        with pytest.raises(ValueError):
            _ = ElevatorOperator(-3)
        elevator_operator = ElevatorOperator(1)
        assert len(elevator_operator.elevators) == 1
        assert len(elevator_operator.waiting_list) == 0

    def test_call_with_one_elevator(self):
        elevator_operator = ElevatorOperator(1)
        passenger = Passenger(3, 5)
        elevator_operator.call(passenger)
        assert len(elevator_operator.waiting_list) == 1
        assert passenger in elevator_operator.waiting_list
        wrong_passenger = Passenger(5, 5)
        with pytest.raises(AssertionError):
            elevator_operator.call(wrong_passenger)
        assert len(elevator_operator.waiting_list) == 1

    def test_find_closest_elevator(self):
        elevators = [Elevator() for _ in range(3)]
        for idx in range(len(elevators)):
            elevators[idx].cur_position = idx * 3
        assert elevators[0] == ElevatorOperator.find_closest_elevator(elevators, Passenger(-1, -10))
        assert elevators[1] == ElevatorOperator.find_closest_elevator(elevators, Passenger(4, 10))
        assert elevators[2] == ElevatorOperator.find_closest_elevator(elevators, Passenger(5, 10))

    def test_idle_elevators(self):
        elevator_operator = ElevatorOperator(3)
        assert len(elevator_operator.idle_elevators()) == 3
        elevator_operator.elevators[1].direction = Direction.UP
        assert len(elevator_operator.idle_elevators()) == 2
        elevator_operator.elevators[1].direction = Direction.STAY
        elevator_operator.elevators[2].direction = Direction.DOWN
        assert len(elevator_operator.idle_elevators()) == 2

    def test_assigning_one_passenger_to_one_elevator(self):
        elevator_operator = ElevatorOperator(1)
        elevator_operator.call(Passenger(1, 5))
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 1
        assert elevator_operator.elevators[0].next_stop == 5
        assert elevator_operator.elevators[0].final_stop == 5
        assert elevator_operator.elevators[0].direction == Direction.UP

    def test_assigning_two_passengers_to_one_elevator(self):
        elevator_operator = ElevatorOperator(1)
        elevator_operator.call(Passenger(1, 5))
        elevator_operator.call(Passenger(2, 7))
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 1
        assert elevator_operator.elevators[0].next_stop == 2
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.UP
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 2
        assert elevator_operator.elevators[0].next_stop == 5
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.UP
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 5
        assert elevator_operator.elevators[0].next_stop == 7
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.UP
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 7
        assert elevator_operator.elevators[0].next_stop == 7
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.STAY

    def test_assigning_two_passengers_to_one_elevator_starting_floor_0(self):
        elevator_operator = ElevatorOperator(1)
        elevator_operator.call(Passenger(0, 5))
        elevator_operator.call(Passenger(2, 7))
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 2
        assert elevator_operator.elevators[0].next_stop == 5
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.UP
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 5
        assert elevator_operator.elevators[0].next_stop == 7
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.UP
        elevator_operator.step()
        assert elevator_operator.elevators[0].cur_position == 7
        assert elevator_operator.elevators[0].next_stop == 7
        assert elevator_operator.elevators[0].final_stop == 7
        assert elevator_operator.elevators[0].direction == Direction.STAY
