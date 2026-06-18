from classes.track import Track

class Event:
    def __init__(self, event_details: list[str], venue: Track, series: str) -> None:
        self.series: str = series
        self.venue: Track = venue

        self.is_oval: bool = venue.track_type == "Speedway" or venue.track_type == "Short Oval"
        # print(f"{self.venue.track_code} '{venue.track_type}' {self.is_oval}")

        self.event_title: str = event_details[0]

        self.event_no: int = int(event_details[1])
        self.order_no: int = int(event_details[2])

        self.race_1_length: int = int(event_details[3])
        if not self.is_oval: self.race_2_length: int = int(event_details[4])

    
    def __str__(self) -> str: return f"Event {self.event_no} - {self.event_title}"