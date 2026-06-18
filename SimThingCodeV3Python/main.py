import math
import os
# import random

from classes.balance_table import BalanceTable
from classes.entrant import Entrant
from classes.event import Event
from classes.series import Series

from data.data import Data
from data.gets import *
from data.sorts import *

from file_handler import *

all_events: list[Event] = []

def valid_int(test: str) -> bool:
    try:
        x = int(test)
        return True
    except ValueError:
        return False

def select_start_event() -> Event:
    for series in Data.series:
        for event in series.calendar:
            all_events.append(event)
    
    for event in all_events:
        print(f"Event {event.order_no} - {event.event_title} ({event.series})")
    
    user_input: str = input("Enter Starting Event: ")
    user_input = user_input.lower().replace("event", "").strip()

    if not valid_int(user_input): return select_start_event()

    user_input: int = int(user_input)

    if user_input < 1: return select_start_event()
    if user_input > len(all_events): return select_start_event()

    return all_events[user_input - 1]

def load_entrants(event: Event) -> list[Entrant]:
    entrants: list[Entrant] = []

    new_entrant: Entrant

    balance_tables: list[BalanceTable] = []
    
    if current_series.do_bop:
        balance_folder: str = os.path.join(Data.series_folder, f"{current_series.series_code} Balance of Performance", f"Event {event.event_no}.csv")

        balance_data: list[str] = read_file(balance_folder)

        for i in range(1, len(balance_data)): balance_tables.append(BalanceTable(balance_data[i].split(',')))

    team: Team

    for entrant in read_file(current_series.entry_list_file):
        entrant_details: list[str] = entrant.split(',')
        if entrant_details[0] != "Car No":
            team = get_team(entrant_details[2], Data.teams)
            new_entrant = Entrant([entrant_details[0], RunningState.RUNNING, get_driver(entrant_details[1], Data.drivers), team])
            new_entrant.set_ovr(event.venue, current_series.do_bop, current_series.log_base, current_series.subtractor, get_balance_table(team.team_code, balance_tables))
            entrants.append(new_entrant)

    return entrants

def reset_teams() -> None:
    for team in Data.teams: team.reserve_available = True

def do_continue() -> bool:
    print("Continue Program?\nY - Yes\nN - No\nR - Reload Data")
    user_input: str = input("Choice: ").upper().strip()

    if user_input == "Y": return True
    if user_input == "N": return False
    if user_input == "R": Data.setup()
    return do_continue()

# Start + Setup

Data.setup()

current_event: Event = select_start_event()
current_series: Series = get_series(current_event.series, Data.series)

continue_simulation: bool = True

while continue_simulation:
    results_folder: str = os.path.join(Data.results_folder, current_series.series_code, current_series.season_folder, f"Event {current_event.event_no} - {current_event.event_title}")
    if not os.path.exists(results_folder): os.mkdir(results_folder)

    print(f"\n{current_event.event_title}")

    current_series.simulate_event(current_event, load_entrants(current_event), results_folder)
    continue_simulation = do_continue()

    if current_event.order_no == len(all_events): break
    if continue_simulation:
        current_event = all_events[current_event.order_no]
        reset_teams()

input("Program Ended\nPress Enter to Exit")