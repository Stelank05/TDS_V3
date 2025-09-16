class Spine:
    def __init__(self, spine_data: list[str]) -> None:
        self.spine_name: str = spine_data[0]
        self.spine_abbr: str = spine_data[1]

        self.chassis: int = int(spine_data[2])
        self.front_sus: int = int(spine_data[3])
        self.rear_sus: int = int(spine_data[4])

        self.total_sus: int = self.front_sus + self.rear_sus
        self.total_ovr: int = self.chassis + self.total_sus

        self.tyre_wear: int = int(spine_data[5])
        self.reliability: int = int(spine_data[6])

    def __str__(self) -> str: return f"{self.spine_name}"
    
    def print_details(self) -> None:
        print(f"Supplier Name: {self.spine_name}")
        print(f"Supplier Abbr: {self.spine_abbr}")
        print(f"Chassis Score: {self.chassis}")
        print(f"Front Sus Score: {self.front_sus}")
        print(f"Rear Sus Score: {self.rear_sus}")
        print(f"Tyre Wear: {self.tyre_wear}")
        print(f"Reliability: {self.reliability}\n")