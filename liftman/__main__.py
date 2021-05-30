from liftman import UserInterface


if __name__ == "__main__":
    eo, floors = UserInterface.initialization()
    UserInterface.user_interface(eo, floors)
