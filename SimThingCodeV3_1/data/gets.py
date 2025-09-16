import math

from classes._import import *

from data.sorts import *

def get_aero_package(package: str, packages: list[AeroPackage], start: int = -1, end: int = -1) -> AeroPackage:
    if start == -1 and end == -1:
        sort_aero_packages(packages)
        start = 0
        end = len(packages)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if packages[middle].package_name == package: return packages[middle]
    elif packages[middle].package_name > package: return get_aero_package(package, packages, start, middle - 1)
    else: return get_aero_package(package, packages, middle + 1, end)

def get_spine(spine: str, spines: list[Spine], start: int = -1, end: int = -1) -> Spine:
    if start == -1 and end == -1:
        sort_spines(spines)
        start = 0
        end = len(spines)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if spines[middle].spine_name == spine: return spines[middle]
    elif spines[middle].spine_name > spine: return get_spine(spine, spines, start, middle - 1)
    else: return get_spine(spine, spines, middle + 1, end)

def get_engine(engine: str, engines: list[Engine], start: int = -1, end: int = -1) -> Engine:
    if start == -1 and end == -1:
        sort_engines(engines)
        start = 0
        end = len(engines)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if engines[middle].engine_name == engine: return engines[middle]
    elif engines[middle].engine_name > engine: return get_engine(engine, engines, start, middle - 1)
    else: return get_engine(engine, engines, middle + 1, end)

def get_tyres(tyre: str, tyres: list[Tyres], start: int = -1, end: int = -1) -> Tyres:
    if start == -1 and end == -1:
        sort_tyres(tyres)
        start = 0
        end = len(tyres)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if tyres[middle].tyre_name == tyre: return tyres[middle]
    elif tyres[middle].tyre_name > tyre: return get_tyres(tyre, tyres, start, middle - 1)
    else: return get_tyres(tyre, tyres, middle + 1, end)

def get_driver(driver: str, drivers: list[Driver], start: int = -1, end: int = -1) -> Driver:
    if start == -1 and end == -1:
        sort_drivers(drivers)
        start = 0
        end = len(drivers)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if drivers[middle].driver_name == driver: return drivers[middle]
    elif drivers[middle].driver_name > driver: return get_driver(driver, drivers, start, middle - 1)
    else: return get_driver(driver, drivers, middle + 1, end)


def get_team(team: str, teams: list[Team], start: int = -1, end: int = -1) -> Team:
    if start == -1 and end == -1:
        sort_teams(teams)
        start = 0
        end = len(teams)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if teams[middle].team_code == team: return teams[middle]
    elif teams[middle].team_code > team: return get_team(team, teams, start, middle - 1)
    else: return get_team(team, teams, middle + 1, end)


def get_track(track: str, tracks: list[Track], start: int = -1, end: int = -1) -> Track:
    if start == -1 and end == -1:
        sort_tracks(tracks)
        start = 0
        end = len(tracks)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if tracks[middle].track_code == track: return tracks[middle]
    elif tracks[middle].track_code > track: return get_track(track, tracks, start, middle - 1)
    else: return get_track(track, tracks, middle + 1, end)

def get_series(series: str, series_list: list[Series], start: int = -1, end: int = -1) -> Series:
    if start == -1 and end == -1:
        sort_series(series_list)
        start = 0
        end = len(series_list)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if series_list[middle].series_name == series: return series_list[middle]
    elif series_list[middle].series_name > series: return get_series(series, series_list, start, middle - 1)
    else: return get_series(series, series_list, middle + 1, end)

def get_event(event: str, events: list[Event], start: int = -1, end: int = -1) -> Event:
    if start == -1 and end == -1:
        sort_events(events)
        start = 0
        end = len(events)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if events[middle].event_title == event: return events[middle]
    elif events[middle].event_title > event: return get_event(event, events, start, middle - 1)
    else: return get_event(event, events, middle + 1, end)

def get_balance_table(table: str, tables: list[BalanceTable], start: int = -1, end: int = -1) -> BalanceTable:
    if start == -1 and end == -1:
        sort_balance_tables(tables)
        start = 0
        end = len(tables)
    
    if start > end: return None

    middle: int = math.floor((start + end) / 2)

    if tables[middle].team_code == table: return tables[middle]
    elif tables[middle].team_code > table: return get_balance_table(table, tables, start, middle - 1)
    else: return get_balance_table(table, tables, middle + 1, end)
