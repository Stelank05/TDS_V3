import os

from classes._import import *

from data.gets import *

from file_handler import *

class Data:
    root_folder: str
    components_folder: str
    series_folder: str
    results_folder: str

    aero_packages: list[AeroPackage] = []
    engine_options: list[Engine] = []
    spine_options: list[Spine] = []
    tyre_options: list[Tyres] = []

    drivers: list[Driver] = []
    teams: list[Team] = []

    tracks: list[Track] = []

    series: list[Series] = []

    def setup() -> None:
        Data.root_folder = os.getcwd().replace("\\SimThingCodeV3_3", "")
        Data.components_folder = os.path.join(Data.root_folder, "V3 Setup Folder", "Components")
        Data.series_folder = os.path.join(Data.root_folder, "V3 Setup Folder", "Series")
        Data.results_folder = os.path.join(Data.root_folder, "Results")

        Data.load_aero_packages()
        Data.load_engine_options()
        Data.load_spine_options()
        Data.load_tyre_options()

        Data.load_drivers()
        Data.load_teams()

        Data.load_tracks()

        Data.load_series()

    def load_aero_packages() -> None:
        Data.aero_packages.clear()

        for aero_package in read_file(os.path.join(Data.components_folder, "Aeros.csv")):
            package_data: list[str] = aero_package.split(',')
            if package_data[0] != "Name": Data.aero_packages.append(AeroPackage(package_data))# ; Data.aero_packages[-1].print_details()

    def load_engine_options() -> None:
        Data.engine_options.clear()

        for engine_supplier in read_file(os.path.join(Data.components_folder, "Engines.csv")):
            supplier_data: list[str] = engine_supplier.split(',')
            if supplier_data[0] != "Name": Data.engine_options.append(Engine(supplier_data))# ; Data.engine_options[-1].print_details()

    def load_spine_options() -> None:
        Data.spine_options.clear()

        for spine_supplier in read_file(os.path.join(Data.components_folder, "Spines.csv")):
            supplier_data: list[str] = spine_supplier.split(',')
            if supplier_data[0] != "Name": Data.spine_options.append(Spine(supplier_data))# ; Data.spine_options[-1].print_details()

    def load_tyre_options() -> None:
        Data.tyre_options.clear()

        for tyre_supplier in read_file(os.path.join(Data.components_folder, "Tyres.csv")):
            supplier_data: list[str] = tyre_supplier.split(',')
            if supplier_data[0] != "Name": Data.tyre_options.append(Tyres(supplier_data))# ; Data.tyre_options[-1].print_details()

    def load_drivers() -> None:
        Data.drivers.clear()

        for driver in read_file(os.path.join(Data.components_folder, "Drivers.csv")):
            driver_data: list[str] = driver.split(',')
            if driver_data[0] != "Name": Data.drivers.append(Driver(driver_data))# ; Data.drivers[-1].print_details()

    def load_teams() -> None:
        Data.teams.clear()

        for team in read_file(os.path.join(Data.components_folder, "Teams.csv")):
            team_data: list[str] = team.split(',')
            if team_data[0] != "Name":
                extras: list[type] = [
                    get_aero_package(team_data[1], Data.aero_packages),
                    get_spine(team_data[8], Data.spine_options),
                    get_engine(team_data[9], Data.engine_options),
                    get_tyres(team_data[10], Data.tyre_options),
                    get_driver(team_data[11], Data.drivers, -1, -1)
                ]
                Data.teams.append(Team(team_data, extras))# ; Data.teams[-1].print_details()
    
    def load_tracks() -> None:
        Data.tracks.clear()

        for track in read_file(os.path.join(Data.components_folder, "Tracks.csv")):
            track_data: list[str] = track.split(',')
            if track_data[0] != "Name": Data.tracks.append(Track(track_data))# ; Data.tracks[-1].print_details()
    
    def load_series() -> None:
        Data.series.clear()

        series_calendar: list[Event]

        for series in read_file(os.path.join(Data.components_folder, "Series.csv")):
            series_data: list[str] = series.split(',')
            if series_data[0] != "Name":
                series_calendar = Data.load_events(os.path.join(Data.series_folder, series_data[3]), series_data[1])
                Data.series.append(Series(series_data, series_calendar, os.path.join(Data.series_folder, series_data[4])))# ; Data.series[-1].print_details()

    def load_events(calendar_file: str, series_name: str) -> list[Event]:
        calendar: list[Event] = []

        for event in read_file(calendar_file):
            event_data: list[str] = event.split(',')
            if event_data[0] != "Title":
                calendar.append(Event(event_data, get_track(event_data[5], Data.tracks), series_name))
    
        return calendar
    