from enum import Enum


class State_machine(Enum):
    """
    Class representing the possible states of the assistant
    WAITING for the user to say the starting phrase
    LISTENING the request of the user
    COMPUTING the request of the user
    """
    WAITING = 1
    LISTENING = 2
    COMPUTING = 3
