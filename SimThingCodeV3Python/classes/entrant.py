import random

from classes.balance_table import BalanceTable
from classes.driver import Driver
from classes.event import Event
from classes.running_state import RunningState
from classes.team import Team
from classes.track import Track

from file_handler import *

class Entrant:
    def __init__(self, entrant_data: list[type]) -> None:
        self.car_no: str = entrant_data[0]

        self.main_ovr: int
        self.backup_ovr: int

        self.practice_boost: int
        self.tyre_performance: int = entrant_data[3].tyres.performance
        self.tyre_life: int

        self.quali_running_pos: int
        self.race_1_grid: int
        self.race_2_grid: int

        self.laps_complete: int = 0
        self.laps_led: int = 0

        self.spine_reliability: int
        self.engine_reliability: int

        self.state: RunningState = entrant_data[1]
        self.dnf_reason: str = "Test"

        self.driver: Driver = entrant_data[2]
        self.team: Team = entrant_data[3]
    
    def set_ovr(self, venue: Track, balance_table: BalanceTable) -> None:
        aero_perf: int = self.team.aero.total_ovr - (balance_table.front_aero + balance_table.rear_aero)
        chassis_perf: int = self.team.spine.chassis - balance_table.chassis
        sus_perf: int = self.team.spine.total_sus
        engine_perf: int = self.team.engine.total_ovr - (balance_table.engine + balance_table.hybrid)

        self.main_ovr = self.driver.driver_score + aero_perf + chassis_perf + sus_perf + engine_perf + self.team.tyres.performance

        match venue.setup_boost:
            case "Aero": self.main_ovr += self.team.aero_setup
            case "Chassis": self.main_ovr += self.team.chassis_setup
            case "Suspension": self.main_ovr += self.team.suspension_setup

        match venue.component_boost:
            case "Aero": self.main_ovr += aero_perf
            case "Chassis": self.main_ovr += chassis_perf
            case "Suspension": self.main_ovr += sus_perf
            case "Engine": self.main_ovr += engine_perf

        self.backup_ovr = self.main_ovr
    
    def do_event(self, session: str) -> bool:
        max_chance: int = 400

        if self.state.value >= 2 and self.state.value <= 4:
            max_chance -= 50
        
        score: int = random.randint(1, max_chance)

        if score <= 2:
            self.state = RunningState.WITHDRAWN
            return True
        if score <= 6:
            self.state = RunningState.NOT_STARTING
            return True
        
        return False

    def replace_driver(self, session: str, new_pos: int) -> None:
        self.team.reserve_available = False

        self.main_ovr = self.backup_ovr - self.driver.driver_score

        self.state = RunningState.RUNNING
        self.driver = self.team.reserve_driver

        self.main_ovr = self.main_ovr + self.driver.driver_score
        self.backup_ovr = self.main_ovr

        if session != "Practice":
            self.practice_boost -= 10
            if self.practice_boost <= 40: self.practice_boost = 40

        if session == "Qualifying":
            self.quali_running_pos = new_pos
        elif session == "Race":
            self.race_1_grid = new_pos
            self.race_2_grid = new_pos

    def create_file_line(self, disp_score: bool, session: str) -> str:
        return_line: str = f"{self.driver.driver_name},{self.car_no},{self.team.team_name},{self.team.spine.spine_abbr},{self.team.engine.engine_abbr},{self.team.tyres.tyre_abbr}"

        if session != "Qualifying": return_line = f"{return_line},{self.laps_complete}"

        if disp_score:
            if self.state.name == "RUNNING": return_line = f"{return_line},{self.main_ovr}"
            else: return_line = f"{return_line},{self.dnf_reason}"
        
        if session == "Race":
            return_line = f"{return_line},,{self.tyre_performance},{self.laps_led}"

        return return_line