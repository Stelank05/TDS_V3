class Tyres:
    def __init__(self, tyre_data: list[str]) -> None:
        self.tyre_name: str = tyre_data[0]
        self.tyre_abbr: str = tyre_data[1]

        self.performance: int = int(tyre_data[2])

        self.degredation: int = int(tyre_data[3])

    def __str__(self) -> str: return f"{self.tyre_name}"
    
    def print_details(self) -> None:
        print(f"Supplier Name: {self.tyre_name}")
        print(f"Supplier Abbr: {self.tyre_abbr}")
        print(f"Performance: {self.performance}")
        print(f"Degredation: {self.degredation}\n")