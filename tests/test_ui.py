from liftman import UserInterface, Elevator


class TestUserInterface:
    def test_visual_ascii_display(self, capsys):
        elevators = [Elevator() for _ in range(3)]
        test_payload = (
            "_______________\n"
            "|    HOTEL    |\n"
            "_______________\n"
            "5|   |   |   ||\n"
            "4|   |   |   ||\n"
            "3|   |   |   ||\n"
            "2|   |   |   ||\n"
            "1|   |   |   ||\n"
            "0| E | E | E ||\n"
            "|__1___2___3__|\n"
        )
        UserInterface.visual_ascii_display(elevators, 5)
        out, err = capsys.readouterr()
        assert out == test_payload
