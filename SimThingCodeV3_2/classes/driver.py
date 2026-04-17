class Driver:
    def __init__(self, driver_data: list[str]) -> None:
        self.driver_name: str = driver_data[0]

        self.driver_score: int = int(driver_data[1])
        self.crash_score: int = int(driver_data[2])
        self.deg_score: int = int(driver_data[3])

    def __str__(self) -> str: return f"{self.driver_name}"
    
    def print_details(self) -> None:
        print(f"Driver Name: {self.driver_name}")
        print(f"Driver Score: {self.driver_score}")
        print(f"Crash Score: {self.crash_score}")
        print(f"Deg Score: {self.deg_score}\n")