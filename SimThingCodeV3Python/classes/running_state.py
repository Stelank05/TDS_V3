from enum import Enum

class RunningState(Enum):
    RUNNING = 1
    CRASHED = 2
    NOT_CLASSIFIED = 3
    RETIRED = 4
    NOT_STARTING = 5
    DISQUALIFIED = 6
    WITHDRAWN = 7
    DID_NOT_QUALIFY = 8