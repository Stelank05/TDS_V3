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
        self.car_ovr: int

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

        self.setup_boost: int = 0
        self.component_boost: int = 0
        self.tyre_wear: int = 0

        self.state: RunningState = entrant_data[1]
        self.dnf_reason: str = "Test"

        self.driver: Driver = entrant_data[2]
        self.team: Team = entrant_data[3]
    
    def set_ovr(self, venue: Track, balance_table: BalanceTable) -> None:
        aero_perf: int = self.team.aero.total_ovr - (balance_table.front_aero + balance_table.rear_aero)
        chassis_perf: int = self.team.spine.chassis - balance_table.chassis
        sus_perf: int = self.team.spine.total_sus
        engine_perf: int = self.team.engine.total_ovr - (balance_table.engine + balance_table.hybrid)

        self.car_ovr = (aero_perf + self.team.aero_setup) + (chassis_perf + self.team.chassis_setup) + (sus_perf + self.team.suspension_setup) + engine_perf #  + self.team.tyres.performance
        # print(f"{self.driver.driver_name}: {aero_perf} + {chassis_perf} + {sus_perf} + {engine_perf} = {self.car_ovr}")

        self.spine_reliability = self.team.spine.reliability + 10
        self.engine_reliability = self.team.engine.reliability + 10
        self.tyre_wear = self.team.tyre_wear + self.team.spine.tyre_wear + self.team.tyres.degredation + self.driver.deg_score

        match venue.setup_boost:
            case "Aero":
                # print(f"Aero Setup: {self.team.aero_setup}")
                self.setup_boost = self.team.aero_setup
            case "Chassis":
                # print(f"Chassis Setup: {self.team.chassis_setup}")
                self.setup_boost = self.team.chassis_setup
            case "Suspension":
                # print(f"Suspension Setup: {self.team.suspension_setup}")
                self.setup_boost = self.team.suspension_setup

        # print(venue.component_boosts)
        for boost in venue.component_boosts:
            # print(boost)
            match boost:
                case "Aero": self.component_boost += aero_perf
                case "Chassis": self.component_boost += chassis_perf
                case "Suspension": self.component_boost += sus_perf
                case "Engine": self.component_boost += engine_perf

        self.car_ovr += self.component_boost + self.setup_boost
        self.main_ovr = self.car_ovr + self.driver.driver_score
        self.backup_ovr = self.main_ovr

        # print(f"{self.driver.driver_name}: {self.car_ovr} ({self.component_boost + self.setup_boost}) / {self.main_ovr}")
    
    def do_event(self, session: str, wdn: list[str], dns: list[str], dnfs: list[str]) -> None:
        max_chance: int = 450

        if session == "Practice":
            max_chance += 100
            wdn.remove("Damage")
        
        if self.dnf_reason not in dnfs and "Damage" in wdn: wdn.remove("Damage")
        else: max_chance += 50

        chance: int = random.randint(1, max_chance)
        # print(f"{self.driver.driver_name} {chance}")

        if chance <= 2:
            self.state = RunningState.WITHDRAWN
            self.dnf_reason = random.choice(wdn)
        elif chance <= 5:
            self.state = RunningState.NOT_STARTING
            self.dnf_reason = random.choice(dns)

    def replace_driver(self, session: str, new_pos: int) -> None:
        self.team.reserve_available = False

        self.main_ovr = self.backup_ovr - self.driver.driver_score

        self.state = RunningState.RUNNING
        self.driver = self.team.reserve_driver

        self.dnf_reason = ""

        self.main_ovr = self.main_ovr + self.driver.driver_score
        self.backup_ovr = self.main_ovr

        if session == "Qualifying Order":
            self.quali_running_pos = new_pos
        elif session == "Race" or session == "Grid":
            print(f"Set Grid to {new_pos}")
            self.race_1_grid = new_pos
            self.race_2_grid = new_pos

    def create_file_line(self, disp_score: bool, session: str) -> str:
        return_line: str = f"{self.driver.driver_name},{self.car_no} {self.team.team_name},{self.team.spine.spine_abbr},{self.team.engine.engine_abbr},{self.team.tyres.tyre_abbr}"

        if session == "Qualifying Order" or session == "Grid": return return_line

        if session != "Qualifying": return_line = f"{return_line},{self.laps_complete}"

        if disp_score:
            if self.state.name == "RUNNING": return_line = f"{return_line},{self.main_ovr}"
            else: return_line = f"{return_line},{self.dnf_reason}"
        
        if session == "Race":
            return_line = f"{return_line},,{self.tyre_performance},{self.laps_led},,{round(self.spine_reliability, 2)},{round(self.engine_reliability, 2)}"

        return return_line