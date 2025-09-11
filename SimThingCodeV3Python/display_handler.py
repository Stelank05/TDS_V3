from classes.aero_package import AeroPackage
from classes.driver import Driver
from classes.engine import Engine
from classes.entrant import Entrant
from classes.running_state import RunningState
from classes.spine import Spine
from classes.team import Team
from classes.tyres import Tyres

class DisplayHandler:
    spacers: list[int] = []

    def set_spacers(entrants: list[Entrant]) -> None: pass
    def display_practice(): pass