from classes.aero_package import AeroPackage
from classes.driver import Driver
from classes.engine import Engine
from classes.spine import Spine
from classes.tyres import Tyres

class Team:
    def __init__(self, team_data: list[str], extras: list[type]) -> None:
        self.team_name: str = team_data[0]
        self.team_code: str = team_data[1]

        self.team_score: int = int(team_data[2])

        self.aero_setup: int = int(team_data[3])
        self.chassis_setup: int = int(team_data[4])
        self.suspension_setup: int = int(team_data[5])

        self.reliability: int = int(team_data[6])
        self.tyre_wear: int = int(team_data[7])

        self.reserve_available: bool = team_data[11].lower() != "none"
        
        self.aero: AeroPackage = extras[0]
        self.spine: Spine = extras[1]
        self.engine: Engine = extras[2]
        self.tyres: Tyres = extras[3]

        self.reserve_driver: Driver = None
        if self.reserve_available: self.reserve_driver = extras[4]

    def __str__(self) -> str: return f"{self.team_code}"
    
    def print_details(self) -> None:
        print(f"Team Name: {self.team_name}")
        print(f"Team Code: {self.team_code}")
        print(f"Team Score: {self.team_score}")
        print(f"Aero Setup: {self.aero_setup}")
        print(f"Chassis Setup: {self.chassis_setup}")
        print(f"Suspension Setup: {self.suspension_setup}")
        print(f"Reliability: {self.reliability}")
        print(f"Tyre Wear: {self.tyre_wear}")
        print(f"Reserve Driver: {self.reserve_driver if self.reserve_available else "-"}")
        print(f"Aero Package Name: {self.aero.package_name}")
        print(f"Spine Supplier: {self.spine.spine_name}")
        print(f"Engine Supplier: {self.engine.engine_name}")
        print(f"Tyre Supplier: {self.tyres.tyre_name}\n")