import json
import os

def read_file(file_path: str) -> list[str]:
    current_file = open(file_path, "r")

    return_data: list[str] = []

    for line in current_file:
        return_data.append(line.replace("\n", "").replace("ï»¿", ""))
    
    return return_data

def write_file(file_path: str, file_data: str) -> None:
    current_file: type

    while True:
        try:
            current_file = open(file_path, "w")
            break
        except IOError:
            input(f"{file_path} Open. Please Close")
    
    with current_file: current_file.write(file_data)

def write_file_old(file_path: str, file_data: str) -> None:
    current_file = open(file_path, "w")
    current_file.write(file_data)
    current_file.close()

def get_files_in_folder(folder_path: str, extension: str) -> list[str]:
    return_files: list[str] = []

    folder = os.walk(folder_path)

    for (root, directories, files) in folder:
        for file in files:
            if extension.lower() in file.lower():
                return_files.append(file)

    return return_files