class Track:
    def __init__(self, track_data: list[str]) -> None:
        self.track_name: str = track_data[0]
        self.track_code: str = track_data[1]
        self.country: str = track_data[2]

        self.track_length: float = float(track_data[3])

        self.incident: int = int(track_data[4])
        self.dnf: int = int(track_data[5])
        self.tyre_wear: int = int(track_data[6])

        self.setup_boost: str = track_data[7]
        self.component_boosts: list[str] = [] # track_data[8]

        for i in range(8, len(track_data)):
            self.component_boosts.append(track_data[i])

        # print(f"{self.track_code}: {self.component_boosts}")

    def __str__(self) -> str: return f"{self.track_code}"
    
    def print_details(self) -> None:
        print(f"Track Name: {self.track_name}")
        print(f"Track Code: {self.track_code}")
        print(f"Country: {self.country}")
        print(f"Track Length: {self.track_length}")
        print(f"Incident: {self.incident}")
        print(f"DNF: {self.dnf}")
        print(f"Tyre Wear: {self.tyre_wear}")
        print(f"Setup Boost: {self.setup_boost}")
        print(f"Component Boost: {self.component_boosts}\n")