from classes.track import Track

class Event:
    def __init__(self, event_details: list[str], venue: Track, series: str) -> None:
        self.event_title: str = event_details[0]
        self.series: str = series

        self.event_no: int = int(event_details[1])
        self.order_no: int = int(event_details[2])

        self.race_1_length: int = int(event_details[3])
        self.race_2_length: int = int(event_details[4])

        self.venue: Track = venue
    
    def __str__(self) -> str: return f"Event {self.event_no} - {self.event_title}"