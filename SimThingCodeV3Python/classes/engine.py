class Engine:
    def __init__(self, engine_data: list[str]) -> None:
        self.engine_name: str = engine_data[0]
        self.engine_abbr: str = engine_data[1]

        self.engine: int = int(engine_data[2])
        self.hybrid: int = int(engine_data[3])

        self.total_ovr: int = self.engine + self.hybrid

        self.reliability: int = int(engine_data[4])

    def __str__(self) -> str: return f"{self.engine_name}"
    
    def print_details(self) -> None:
        print(f"Supplier Name: {self.engine_name}")
        print(f"Supplier Abbr: {self.engine_abbr}")
        print(f"Engine Score: {self.engine}")
        print(f"Hybrid Score: {self.hybrid}")
        print(f"Reliability: {self.reliability}\n")
