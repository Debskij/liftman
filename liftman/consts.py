elevator_emoji = "E"
final_floor_emoji = "F"
next_floor_emoji = "N"

prompt = {
    "e_no": "Amount of elevators in building: ",
    "f_no": "Amount of floors in building: ",
    "p_floor": "Floor that passenger will be taken from: ",
    "d_floor": "Floor that passenger will be taken to: ",
    "decision": "What do you want to do? ",
}

messages = {
    "z_pas": "There is not even single spirit without assigned elevator",
    "pos_error": "Error! Destination floor cant be same as current position",
    "b_val": "Invalid value passed",
    "d_step": "Step done",
    "f_step": "No more floors to travel",
}

help_msg = (
    "\n_______________________________________________________________________\n"
    "Commands description\n"
    "a: All passengers that are not assigned to elevator are displayed.\n"
    "b: Break the program and exit the program.\n"
    "c: Call elevator for new passenger.\n"
    "d: Display whole building status with elevators.\n"
    "e: Elevators will do a step.\n"
    "f: Full description of each elevator stops (passengers that are travelling)"
)
