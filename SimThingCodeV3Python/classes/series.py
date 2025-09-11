import os
import random

from classes.entrant import Entrant
from classes.event import Event
from classes.running_state import RunningState

from file_handler import *

class Series:
    grid_spacer: int = 5

    min_stint: int = 35
    max_stint: int = 70

    min_incident: int = 5
    max_incident: int = 100
    min_dnf: int = 5
    max_dnf: int = 15

    dnf_reasons: list[str] = ["Crash", "Collision", "Engine", "Hybrid", "Gearbox", "Suspension", "Electronics", "Fuel System", "Tyre Failure"]
    dns_reasons: list[str] = ["Engine", "Hybrid", "Gearbox", "Electronics", "Fuel System"]
    dsq_reasons: list[str] = ["Underweight", "Wing Flex", "Illegal Part", "Fuel Sample", "Plank Wear"]
    wdn_reasons: list[str] = ["Illness", "Injury", "Damage"]

    def __init__(self, series_data: list[str], calendar: list[Event], entry_list_file: str) -> None:
        self.series_name: str = series_data[0]
        self.series_code: str = series_data[1]
        self.season_folder: str = series_data[2]

        self.calendar_file: str = series_data[3]
        self.entry_list_file: str = entry_list_file

        self.calendar: list[Event] = calendar

        # Event Data
        self.session: str
        self.file_number: int

        self.current_event: Event
        self.event_folder: str

        self.race_length: int
        self.race_over: bool = False

        self.entrants: list[Entrant]
        self.spacers: list[int]

    def __str__(self) -> str: return f"{self.series_code}"

    def print_details(self) -> None:
        print(f"Series Name: {self.series_name}")
        print(f"Series Code: {self.series_code}")
        print(f"Results Folder: {self.season_folder}")
        print(f"Calendar File: {self.calendar_file}")
        print(f"Calendar ({len(self.calendar)} Events):")
        for event in self.calendar: print(f" {event}")

    def simulate_event(self, event: Event, entrants: list[Entrant], event_folder: str) -> None:
        self.current_event = event
        self.event_folder = event_folder
        self.file_number = 1
        
        self.session = "Practice"

        self.entrants = entrants.copy()
        self.set_spacers()
        # print(len(self.entrants))

        # Maybe a way for drivers to be replaced before practice?
        self.do_events()


        self.simulate_practice()
        Series.sort_entrants_ovr(self.entrants)
        print("\nPractice Results:")
        self.display_entrants(0, len(self.entrants), )
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Practice Results.csv")); self.file_number += 1
        input()

        self.session = "Qualifying"
        
        self.set_qualifying_order()
        print("Qualifying Order:")
        self.display_entrants(0, len(self.entrants), False, False)
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Qualifying Running Order.csv"), False); self.file_number += 1
        input()

        self.simulate_qualifying_1()
        Series.sort_entrants_ovr(self.entrants)
        Series.sort_entrants_state(self.entrants)
        self.set_race_2_grid()
        print("Qualifying 1 Results:")
        self.display_entrants(0, len(self.entrants), False)
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Qualifying 1 Results.csv")); self.file_number += 1
        input()

        self.simulate_qualifying_2()
        Series.sort_entrants_ovr(self.entrants, 0, 10)
        Series.sort_entrants_state(self.entrants, 0, 10)
        self.set_race_1_grid()
        print("Qualifying 2 Results:")
        self.display_entrants(0, 10, False)
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Qualifying 2 Results.csv"), end = 10); self.file_number += 1
        input()

        # Display Provisional Qualifying Results
        print("Provisional Qualifying Results:")
        self.display_entrants(0, len(self.entrants), False)
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Provisional Qualifying Results.csv")); self.file_number += 1
        input()

        # Scrutineering
        self.scrutineering()
        if len(self.entrants) > 30: self.set_non_starters()

        # Display Final Qualifying Results
        print("Final Qualifying Results:")
        self.display_entrants(0, len(self.entrants), False)
        self.save_entrants(os.path.join(event_folder, f"{self.file_number} - Final Qualifying Results.csv")); self.file_number += 1
        input()
        
        self.session = "Race"

        # Drop Entries
        if len(self.entrants) > 30: self.drop_entrants()

        # Race 1
        self.simulate_race("Race 1")

        # Race 2
        self.simulate_race("Race 2")
        

    # Simulation
    def simulate_lap(self, entrant: Entrant) -> tuple[int]:
        min_stint: int = Series.min_stint + entrant.driver.driver_score + entrant.tyre_performance
        max_stint: int = Series.max_stint + entrant.driver.driver_score + entrant.tyre_performance

        min_incident: int = Series.min_incident + entrant.driver.crash_score
        max_incident: int = Series.max_incident + entrant.driver.crash_score + self.current_event.venue.incident
        max_dnf: int = Series.max_dnf + entrant.driver.crash_score + self.current_event.venue.dnf

        min_tyre_wear: int = self.current_event.venue.tyre_wear + entrant.team.tyre_wear + entrant.team.spine.tyre_wear + entrant.team.tyres.degredation + entrant.driver.deg_score
        max_tyre_wear: int = min_tyre_wear + (3 * entrant.driver.deg_score)

        if self.session == "Practice": max_incident += entrant.driver.crash_score + self.current_event.venue.incident

        if self.session == "Qualifying":
            min_stint += entrant.practice_boost
            max_stint += entrant.practice_boost

        stint_score: int = random.randint(min_stint, max_stint)
        tyre_wear: int = random.randint(min_tyre_wear, max_tyre_wear)
        incident: int = random.randint(min_incident, max_incident)

        if incident < Series.min_incident + (2 * entrant.driver.crash_score):
            dnf: int = random.randint(Series.min_dnf, max_dnf)

            if dnf == Series.min_dnf: return 1, 0
            else:
                stint_score -= dnf
                if stint_score < min_stint: stint_score = min_stint
                return stint_score, tyre_wear + int(dnf / 3)
        
        return stint_score, tyre_wear

    def simulate_race_lap(self, entrant: Entrant, laps_remaining: int) -> list[int]:
        min_stint: int = Series.min_stint + entrant.driver.driver_score + entrant.tyre_performance + entrant.practice_boost
        max_stint: int = Series.max_stint + entrant.driver.driver_score + entrant.tyre_performance + entrant.practice_boost

        min_incident: int = Series.min_incident + entrant.driver.crash_score
        max_incident: int = Series.max_incident + entrant.driver.crash_score + self.current_event.venue.incident
        max_dnf: int = Series.max_dnf + entrant.driver.crash_score + self.current_event.venue.dnf

        min_tyre_wear: int = self.current_event.venue.tyre_wear + entrant.team.tyre_wear + entrant.team.spine.tyre_wear + entrant.team.tyres.degredation + entrant.driver.deg_score
        max_tyre_wear: int = min_tyre_wear + (3 * entrant.driver.deg_score)

        stint: int = random.randint(min_stint, max_stint)
        tyre_wear: int = random.randint(min_tyre_wear, max_tyre_wear)
        incident: int = random.randint(min_incident, max_incident)
        pitstop: int = 0

        min_tyre_perf: int = entrant.team.tyres.performance - 50
        max_tyre_perf: int = entrant.team.tyres.performance - 35

        if laps_remaining < 6:
            min_tyre_perf -= 5
            max_tyre_perf -= 5

        if entrant.tyre_performance < random.randint(min_tyre_perf, max_tyre_perf):
            pitstop = random.randint(45, 55)
            tyre_wear -= 2

            if tyre_wear <= 0: tyre_wear = 1
        
        if incident < min_incident + (3 * entrant.driver.crash_score):
            dnf: int = random.randint(Series.min_dnf, max_dnf)

            if dnf == Series.min_dnf:
                return [1, 0, 0]
            else:
                stint -= dnf

                if stint < min_stint:
                    stint = min_stint
        
        return [stint, int(tyre_wear / 4), pitstop]

    def simulate_practice(self) -> None:
        laps: int; stint_total: int; stint_avg: int
        results: tuple[int]

        for entrant in self.entrants:
            if entrant.state == RunningState.RUNNING:
                laps = random.randint(15, 20)
                stint_total = 0

                while entrant.laps_complete < laps:
                    results = self.simulate_lap(entrant)

                    if results[0] == 1:
                        entrant.state = RunningState.CRASHED
                        Series.set_dnf_reason(entrant)
                        # print(f"{entrant.driver.driver_name} INCIDENT {entrant.dnf_reason}")
                        break
                    else:
                        entrant.laps_complete += 1
                        stint_total += results[0]

                        if entrant.backup_ovr + results[0] > entrant.main_ovr:
                            entrant.main_ovr = entrant.backup_ovr + results[0]
            
            if entrant.laps_complete == 0: stint_avg = 0
            else: stint_avg = int(stint_total / entrant.laps_complete)
            
            entrant.practice_boost = int(stint_avg / 5)

    def set_qualifying_order(self) -> None:
        positions: list[int] = list(range(len(self.entrants)))
        position: int

        for entrant in self.entrants:
            position = random.choice(positions)
            positions.remove(position)
            entrant.quali_running_pos = position

            entrant.state = RunningState.RUNNING
            entrant.main_ovr = entrant.backup_ovr

            entrant.do_event("Qualifying")

            if entrant.state == RunningState.WITHDRAWN:
                Series.set_wdn_reason(entrant)
                if entrant.team.reserve_available: self.replace_driver(entrant)
            elif entrant.state == RunningState.NOT_STARTING:
                Series.set_dns_reason(entrant)

        Series.sort_entrants_quali(self.entrants)
        
    def simulate_qualifying_1(self) -> None:
        results: tuple[int]

        for entrant in self.entrants:
            if entrant.state == RunningState.RUNNING:
                results = self.simulate_lap(entrant)

                if results[0] == 1:
                    entrant.state = RunningState.CRASHED
                    Series.set_dnf_reason(entrant)
                    # print(f"{entrant.driver.driver_name} INCIDENT {entrant.dnf_reason}")
                else:
                    entrant.main_ovr = entrant.backup_ovr + results[0]

    def simulate_qualifying_2(self) -> None:
        entrant: Entrant
        results: tuple[int]

        i = 9
        while i >= 0:
            entrant = self.entrants[i]
            
            if entrant.state == RunningState.RUNNING:
                results = self.simulate_lap(entrant)

                if results[0] == 1:
                    entrant.state = RunningState.CRASHED
                    Series.set_dnf_reason(entrant)
                    # print(f"{entrant.driver.driver_name} INCIDENT {entrant.dnf_reason}")
                else:
                    entrant.main_ovr = entrant.backup_ovr + results[0]
            
            i -= 1

    def set_grid(self) -> None:
        entrant: Entrant

        for i in range(len(self.entrants)):
            entrant = self.entrants[i]

            entrant.laps_complete = 0
            entrant.laps_led = 0
            entrant.tyre_life = 100

            if not (entrant.state == RunningState.WITHDRAWN or entrant.state == RunningState.DID_NOT_QUALIFY):
                entrant.state = RunningState.RUNNING

            if entrant.state == RunningState.RUNNING:
                entrant.main_ovr = entrant.backup_ovr + ((len(self.entrants) - i) * Series.grid_spacer)

    def simulate_race(self, race_number: str) -> None:
        race_folder: str = os.path.join(self.event_folder, race_number)
        if not os.path.exists(race_folder): os.mkdir(race_folder)

        file_number: int = 1
        self.race_over = False

        self.do_events()

        if race_number == "Race 1":
            Series.sort_entrants_race_1(self.entrants)
            self.race_length = self.current_event.race_1_length
        else:
            Series.sort_entrants_race_2(self.entrants)
            self.race_length = self.current_event.race_2_length
        
        self.set_grid()
        Series.sort_entrants_state(self.entrants)

        print(f"{race_number} Grid:")
        self.display_entrants(0, len(self.entrants))
        self.save_entrants(os.path.join(race_folder, f"{file_number} - Grid.csv")); file_number += 1
        input()

        stint: list[int]

        for lap in range(self.race_length):
            for entrant in self.entrants:
                if entrant.state == RunningState.RUNNING:
                    stint = self.simulate_race_lap(entrant, self.race_length - lap + 1)

                    if stint[2] > 0:
                        entrant.tyre_performance = entrant.team.tyres.performance
                        entrant.tyre_life = 100 - stint[1]

                        entrant.tyre_performance = entrant.team.tyres.performance - int((100 - entrant.tyre_life) * ((entrant.team.tyres.degredation + 1) / 2))
                    else:
                        entrant.tyre_life -= stint[1]

                        entrant.tyre_performance = entrant.team.tyres.performance - int((100 - entrant.tyre_life) * ((entrant.team.tyres.degredation + 1) / 2))                        
                    
                    entrant.laps_complete += 1

                    if stint[0] > 1:
                        entrant.main_ovr += (stint[0] - stint[1])
                    else:
                        if lap + 1>= self.race_length - 3:
                            entrant.state = RunningState.NOT_CLASSIFIED
                        else:
                            entrant.state = RunningState.RETIRED

                        Series.set_dnf_reason(entrant)
            
            Series.sort_entrants_state(self.entrants)
            Series.sort_entrants_ovr_r(self.entrants)
            self.entrants[0].laps_led += 1

            self.race_over = True

            print(f"{race_number}: Lap {lap + 1}/{self.race_length}:")
            self.display_entrants(0, len(self.entrants))
            self.save_entrants(os.path.join(race_folder, f"{file_number} - Lap {lap + 1}.csv")); file_number += 1
            input()
        
        self.scrutineering()
        print(f"{race_number} Final Results:")
        self.display_entrants(0, len(self.entrants))
        self.save_entrants(os.path.join(race_folder, f"{file_number} - Race Results.csv"))
        input()


    # Post Qualifying
    def set_race_1_grid(self) -> None:
        for i in range(len(self.entrants)):
            self.entrants[i].race_1_grid = i

    def set_race_2_grid(self) -> None:
        for i in range(len(self.entrants)):
            self.entrants[i].race_2_grid = i
            
    def scrutineering(self) -> None:
        result: int

        for entrant in self.entrants:
            if entrant.state == RunningState.RUNNING:
                result = random.randint(1, 250)

                if result == 1:
                    entrant.state = RunningState.DISQUALIFIED
                    Series.set_dsq_reason(entrant)

                    if self.session == "Qualifying":
                        entrant.race_1_grid = len(self.entrants)
                        entrant.race_2_grid = len(self.entrants)
        
        Series.sort_entrants_state(self.entrants)

    def set_non_starters(self) -> None:
        for i in range(30, len(self.entrants)):
            self.entrants[i].state = RunningState.DID_NOT_QUALIFY

    def drop_entrants(self) -> None:
        while len(self.entrants) > 30:
            self.entrants.remove(self.entrants[-1])


    # Entrant Actions
    def set_dnf_reason(entrant: Entrant) -> None: entrant.dnf_reason = random.choice(Series.dnf_reasons)
    def set_dns_reason(entrant: Entrant) -> None: entrant.dnf_reason = random.choice(Series.dns_reasons)
    def set_dsq_reason(entrant: Entrant) -> None: entrant.dnf_reason = random.choice(Series.dsq_reasons)
    def set_wdn_reason(entrant: Entrant) -> None: entrant.dnf_reason = random.choice(Series.wdn_reasons)
    
    def do_events(self) -> None:
        for entrant in self.entrants:
            if entrant.do_event("Race"):
                if entrant.state == RunningState.WITHDRAWN:
                    Series.set_wdn_reason(entrant)
                    if entrant.team.reserve_available: self.replace_driver(entrant)
                elif entrant.state == RunningState.NOT_STARTING:
                    Series.set_dns_reason(entrant)

    def replace_driver(self, entrant: Entrant) -> None:
        if entrant.dnf_reason == "Damage": return None

        print(f"REPLACE {entrant.driver.driver_name} WITH {entrant.team.reserve_driver.driver_name} ({entrant.dnf_reason})")
        entrant.replace_driver(self.session, len(self.entrants) + 1)
        self.set_spacers()


    # Sorts
    def sort_entrants_ovr(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)

        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j].main_ovr < entrants[j + 1].main_ovr:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break

    def sort_entrants_ovr_r(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)

        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j + 1].state != RunningState.RUNNING: break

                if entrants[j].main_ovr < entrants[j + 1].main_ovr:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break

    def sort_entrants_state(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)
            
        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j].state.value > entrants[j + 1].state.value:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break

    def sort_entrants_quali(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)
            
        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j].quali_running_pos > entrants[j + 1].quali_running_pos:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break

    def sort_entrants_race_1(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)
            
        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j].race_1_grid > entrants[j + 1].race_1_grid:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break

    def sort_entrants_race_2(entrants: list[Entrant], start: int = -1, end: int = -1) -> None:
        if start == -1 and end == -1:
            start = 0
            end = len(entrants)
            
        swap: bool

        for i in range(end - 1):
            swap = False

            for j in range(start, end - i - 1):
                if entrants[j].race_2_grid > entrants[j + 1].race_2_grid:
                    swap = True
                    entrants[j], entrants[j + 1] = entrants[j + 1], entrants[j]

            if not swap: break


    # Display
    def set_spacers(self) -> None:
        self.spacers = [len(self.entrants[0].driver.driver_name), len(self.entrants[0].team.team_code)]
        
        for i in range(1, len(self.entrants)):
            if len(self.entrants[i].driver.driver_name) > self.spacers[0]: self.spacers[0] = len(self.entrants[i].driver.driver_name)
            if len(self.entrants[i].team.team_code) > self.spacers[1]: self.spacers[1] = len(self.entrants[i].team.team_code)

    def display_entrants(self, start: int, end: int, disp_tyre: bool = True, disp_score: bool = True) -> None:
        tyres: str = ""
        inc: str = ""

        entrant: Entrant

        for i in range(start, end):
            entrant = self.entrants[i]

            if disp_tyre: tyres = f" - {str(entrant.tyre_performance).ljust(3, ' ')}"
            if disp_score:
                if entrant.state.name == "RUNNING": inc = f" - {str(entrant.main_ovr).ljust(len(str(self.entrants[0].main_ovr)), ' ')}"
                else:
                    inc = f" - {str(entrant.main_ovr).ljust(len(str(self.entrants[0].main_ovr)), ' ')} ({entrant.dnf_reason})"
                    if self.session == "Race": inc = f"{inc} ({entrant.laps_complete})"
                
                if self.session == "Race" and entrant.laps_led > 0: inc = f"{inc} ({entrant.laps_led})"
            
            print(f"{self.get_pos(entrant, i + 1).ljust(3, ' ')}: {Series.center(entrant.driver.driver_name, self.spacers[0])} - {entrant.car_no.ljust(3, ' ')} {Series.center(entrant.team.team_code, self.spacers[1])} - {entrant.team.spine.spine_abbr}/{entrant.team.engine.engine_abbr}/{entrant.team.tyres.tyre_abbr}{tyres}{inc}")


    # Save File
    def save_entrants(self, file_name: str, disp_score: bool = True, start: int = 0, end: int = -1) -> None:
        if end == -1: end = len(self.entrants)

        write_string: str = f"{self.get_pos(self.entrants[start], 1)},{self.entrants[start].create_file_line(disp_score, self.session)}"

        for i in range(start + 1, end):
            write_string += f"\n{self.get_pos(self.entrants[i], i + 1)},{self.entrants[i].create_file_line(disp_score, self.session)}"
        
        write_file(file_name, write_string)


    # Generic
    def get_pos(self, entrant: Entrant, place: int) -> str:
        pos: str

        match entrant.state:
            case RunningState.RUNNING: pos = f"P{place}"
            case RunningState.CRASHED: pos = "INC"
            case RunningState.NOT_CLASSIFIED:
                if not self.race_over: pos = "DNF"
                elif self.session == "Race" and entrant.laps_complete == self.race_length: pos = f"P{place}"
                else: pos = "NC"
            case RunningState.RETIRED: pos = "DNF"
            case RunningState.NOT_STARTING: pos = "DNS"
            case RunningState.DISQUALIFIED:
                if self.session == "Qualifying": pos = "EXC"
                else: pos = "DSQ"
            case RunningState.WITHDRAWN: pos = "WDN"
            case RunningState.DID_NOT_QUALIFY: pos = "DNQ"
        
        return pos

    def center(text: str, spacer: int) -> str:
        side: int = 0

        while len(text) < spacer:
            if side % 2 == 0: text = f" {text}"
            else: text = f"{text} "
            side += 1
        
        return text
