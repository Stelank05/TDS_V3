class BalanceTable:
    def __init__(self, balance_details: list[str]) -> None:
        self.team_code: str = balance_details[0]

        self.front_aero: int = int(balance_details[1])
        self.rear_aero: int = int(balance_details[2])

        self.chassis: int = int(balance_details[3])

        self.engine: int = int(balance_details[4])
        self.hybrid: int = int(balance_details[5])