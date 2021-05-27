from pytest import raises, fixture
from liftman import Direction, Passenger


class TestHelpers:
    @fixture()
    def up_passenger(self):
        return Passenger(3, 5)

    @fixture()
    def down_passenger(self):
        return Passenger(5, 3)

    @fixture()
    def stay_passenger(self):
        return Passenger(3, 3)

    def test_directions(self):
        up, down, stay = Direction.UP, Direction.DOWN, Direction.STAY
        assert up.name == "UP" and up.value == 1
        assert down.name == "DOWN" and down.value == -1
        assert stay.name == "STAY" and stay.value == 0

    def test_passenger_initialization(self):
        passenger = Passenger(3, 5)
        assert passenger.position == 3
        assert passenger.destination == 5

    def test_passenger_direction(self, up_passenger, down_passenger):
        assert up_passenger.direction() == Direction.UP
        assert down_passenger.direction() == Direction.DOWN

    def test_invalid_passenger_direction(self, stay_passenger):
        with raises(ValueError):
            _ = stay_passenger.direction()

    def test_amount_of_floors_negative(self, up_passenger):
        assert up_passenger.amount_of_floors() == 2

    def test_amount_of_floors_positive(self, down_passenger):
        assert down_passenger.amount_of_floors() == 2
