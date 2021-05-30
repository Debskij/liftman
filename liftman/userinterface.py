import os

from liftman import ElevatorOperator, Passenger, Elevator
from typing import List, Tuple, Dict, Callable
from liftman.consts import prompt, messages, elevator_emoji, final_floor_emoji, next_floor_emoji, help_msg


class UserInterface:
    @staticmethod
    def visual_ascii_display(e: List[Elevator], height: int):
        width = 3 + len(e) * 4

        def find_all_statuses(floor: int) -> str:
            return str(floor) + "".join([f"| {symbol_for_position(elevator, floor)} " for elevator in e]) + "||"

        def symbol_for_position(elevator: Elevator, floor: int) -> str:
            if elevator.cur_position == floor:
                return elevator_emoji
            elif elevator.final_stop == floor:
                return final_floor_emoji
            elif elevator.next_stop == floor:
                return next_floor_emoji
            else:
                return " "

        def banner() -> str:
            return (
                "_" * width
                + "\n"
                + "|"
                + (len(e) - 1) * 2 * " "
                + "HOTEL"
                + (len(e) - 1) * 2 * " "
                + "|"
                + "\n"
                + "_" * width
                + "\n"
            )

        def elevators() -> str:
            return "\n".join([find_all_statuses(floor) for floor in range(height, -1, -1)])

        def parquet() -> str:
            return "\n" + "|" + "".join([f"__{e_no}_" for e_no in range(1, len(e) + 1)]) + "_|"

        print(banner() + elevators() + parquet())

    @staticmethod
    def show_passangers_for_all_elevators(elevator_operator: ElevatorOperator):
        print("\n".join([f"{idx+1}. {elevator.stops}" for idx, elevator in enumerate(elevator_operator.elevators)]))

    @staticmethod
    def validate_value(lower_bound, upper_bound, type_cast, input_prompt: str):
        while True:
            value = input(input_prompt)
            try:
                value = type_cast(value)
                if lower_bound <= value <= upper_bound:
                    return value
                raise ValueError
            except ValueError:
                print(messages["b_val"])

    @staticmethod
    def initialization() -> Tuple[ElevatorOperator, int]:
        os.system("cls" if os.name == "nt" else "clear")
        elevators_no = UserInterface.validate_value(1, 1000, int, prompt["e_no"])
        floors_no = UserInterface.validate_value(1, 1000, int, prompt["f_no"])
        return ElevatorOperator(elevators_no), floors_no

    @staticmethod
    def passenger_call(elevator_operator: ElevatorOperator, height: int):
        while True:
            pos_floor = UserInterface.validate_value(0, height, int, prompt["p_floor"])
            dest_floor = UserInterface.validate_value(0, height, int, prompt["d_floor"])
            if dest_floor != pos_floor:
                new_passenger = Passenger(pos_floor, dest_floor)
                elevator_operator.call(new_passenger)
                print(f"Added passenger {new_passenger} to waiting list")
                return
            else:
                print(messages["pos_error"])

    @staticmethod
    def do_step(elevator_operator: ElevatorOperator) -> None:
        if elevator_operator.step():
            print(messages["d_step"])
        else:
            print(messages["f_step"])
        return

    @staticmethod
    def display_all_waiting_passengers(elevator_operator: ElevatorOperator):
        if len(elevator_operator.waiting_list) > 0:
            print(
                "\n".join(
                    [f"{idx + 1}. {str(passenger)}" for idx, passenger in enumerate(elevator_operator.waiting_list)]
                )
            )
        else:
            print(messages["z_pas"])

    @staticmethod
    def user_interface(elevator_operator: ElevatorOperator, height: int):
        commands: Dict[str, Callable] = {
            "a": UserInterface.display_all_waiting_passengers,
            "c": UserInterface.passenger_call,
            "d": UserInterface.visual_ascii_display,
            "e": UserInterface.do_step,
            "f": UserInterface.show_passangers_for_all_elevators,
        }
        args: Dict[str, List] = {
            "a": [elevator_operator],
            "c": [elevator_operator, height],
            "d": [elevator_operator.elevators, height],
            "e": [elevator_operator],
            "f": [elevator_operator],
        }
        while True:

            print(help_msg)
            cmd = UserInterface.validate_value("a", "f", str, prompt["decision"])
            os.system("cls" if os.name == "nt" else "clear")
            if cmd == "b":
                return
            else:
                commands[cmd](*args[cmd])
