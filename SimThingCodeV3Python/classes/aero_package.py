class AeroPackage:
    def __init__(self, package_details: list[str]) -> None:
        self.package_name: str = package_details[0]

        self.front_aero: int = int(package_details[1])
        self.rear_aero: int = int(package_details[2])
        self.floor: int = int(package_details[3])
        self.sidepods: int = int(package_details[4])

        self.total_ovr: int = self.front_aero + self.rear_aero + self.floor + self.sidepods

    def __str__(self) -> str: return f"{self.package_name}"
    
    def print_details(self) -> None:
        print(f"Package Name: {self.package_name}")
        print(f"Front Aero: {self.front_aero}")
        print(f"Rear Aero: {self.rear_aero}")
        print(f"Floor: {self.floor}")
        print(f"Sidepods: {self.sidepods}\n")
