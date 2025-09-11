from classes._import import *

def sort_aero_packages(packages: list[AeroPackage]) -> None:
    swap: bool

    for i in range(len(packages) - 1):
        swap = False

        for j in range(len(packages) - i - 1):
            if packages[j].package_name > packages[j + 1].package_name:
                swap = True
                packages[j], packages[j + 1] = packages[j + 1], packages[j]

        if not swap: break

def sort_spines(spines: list[Spine]) -> None:
    swap: bool

    for i in range(len(spines) - 1):
        swap = False

        for j in range(len(spines) - i - 1):
            if spines[j].spine_name > spines[j + 1].spine_name:
                swap = True
                spines[j], spines[j + 1] = spines[j + 1], spines[j]

        if not swap: break

def sort_engines(engines: list[Engine]) -> None:
    swap: bool

    for i in range(len(engines) - 1):
        swap = False

        for j in range(len(engines) - i - 1):
            if engines[j].engine_name > engines[j + 1].engine_name:
                swap = True
                engines[j], engines[j + 1] = engines[j + 1], engines[j]

        if not swap: break

def sort_tyres(tyres: list[Tyres]) -> None:
    swap: bool

    for i in range(len(tyres) - 1):
        swap = False

        for j in range(len(tyres) - i - 1):
            if tyres[j].tyre_name > tyres[j + 1].tyre_name:
                swap = True
                tyres[j], tyres[j + 1] = tyres[j + 1], tyres[j]

        if not swap: break

def sort_drivers(drivers: list[Driver]) -> None:
    swap: bool

    for i in range(len(drivers) - 1):
        swap = False

        for j in range(len(drivers) - i - 1):
            if drivers[j].driver_name > drivers[j + 1].driver_name:
                swap = True
                drivers[j], drivers[j + 1] = drivers[j + 1], drivers[j]

        if not swap: break

def sort_teams(teams: list[Team]) -> None:
    swap: bool

    for i in range(len(teams) - 1):
        swap = False

        for j in range(len(teams) - i - 1):
            if teams[j].team_code > teams[j + 1].team_code:
                swap = True
                teams[j], teams[j + 1] = teams[j + 1], teams[j]

        if not swap: break

def sort_tracks(tracks: list[Track]) -> None:
    swap: bool

    for i in range(len(tracks) - 1):
        swap = False

        for j in range(len(tracks) - i - 1):
            if tracks[j].track_code > tracks[j + 1].track_code:
                swap = True
                tracks[j], tracks[j + 1] = tracks[j + 1], tracks[j]

        if not swap: break

def sort_series(series: list[Series]) -> None:
    swap: bool

    for i in range(len(series) - 1):
        swap = False

        for j in range(len(series) - i - 1):
            if series[j].series_name > series[j + 1].series_name:
                swap = True
                series[j], series[j + 1] = series[j + 1], series[j]

        if not swap: break

def sort_events(events: list[Event]) -> None:
    swap: bool

    for i in range(len(events) - 1):
        swap = False

        for j in range(len(events) - i - 1):
            if events[j].event_title > events[j + 1].event_title:
                swap = True
                events[j], events[j + 1] = events[j + 1], events[j]

        if not swap: break

def order_events(events: list[Event]) -> None:
    swap: bool

    for i in range(len(events) - 1):
        swap = False

        for j in range(len(events) - i - 1):
            if events[j].order_no > events[j + 1].order_no:
                swap = True
                events[j], events[j + 1] = events[j + 1], events[j]

        if not swap: break

def sort_balance_tables(tables: list[BalanceTable]) -> None:
    swap: bool

    for i in range(len(tables) - 1):
        swap = False

        for j in range(len(tables) - i - 1):
            if tables[j].team_code > tables[j + 1].team_code:
                swap = True
                tables[j], tables[j + 1] = tables[j + 1], tables[j]

        if not swap: break

