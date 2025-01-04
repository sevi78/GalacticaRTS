import datetime
import glob
import os

import send2trash

dirpath = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "pictures" + os.sep
gifs_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "gifs" + os.sep
soundpath = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "sounds" + os.sep





def update_dict(data, default_dict):
    keys_to_delete = []
    for key in data:
        if key not in default_dict:
            keys_to_delete.append(key)
        elif isinstance(data[key], dict) and isinstance(default_dict[key], dict):
            update_dict(data[key], default_dict[key])

    for key in keys_to_delete:
        del data[key]

    for key, value in default_dict.items():
        if key not in data:
            data[key] = value


def update_json_files(default_dict):
    # Full path to the 'database' directory
    path = abs_level_path()

    # Use os.path.join to create the full path to the .json files
    full_path = os.path.join(path, '*.json')

    # Iterate over all .json files in the 'database' directory
    for filename in glob.glob(full_path):
        # Open and load the JSON file
        with open(filename, 'r') as file:
            data = json.load(file)

        # Update the data with the default dictionary
        level = int(os.path.basename(filename).split("_")[1].split(".json")[0])
        update_dict(data, default_dict)
        data["globals"]["level"] = level
        # Write the updated data back to the file
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)


def compare_json_files(folder, default_file):
    for file_name in os.listdir(folder):
        if file_name.endswith('.json'):
            with open(os.path.join(folder, file_name)) as json_file:
                data = json.load(json_file)
                print(f"Comparing file: {file_name}")
                compare_json(default_file, data, file_name)


def update_files(folder, category, key, value, **kwargs):
    condition = kwargs.get('condition', "1=1")
    # get path
    path = os.path.join(abs_database_path() + os.sep + folder)

    # search files
    for file_name in os.listdir(path):
        if file_name.endswith('.json'):

            # open file
            with open(os.path.join(path, file_name)) as json_file:
                data = json.load(json_file)

                # search for key
                for k, v in data[category].items():
                    # add key
                    if not key in data[category][k]:
                        data[category][k][key] = value

                    else:
                        if condition and eval(condition):
                            data[category][k][key] = value
                        else:
                            data[category][k][key] = -1

            write_file(file_name, folder, data)


def update_level_files(folder, category, key, value):
    # get path
    path = os.path.join(abs_database_path() + os.sep + folder)

    # search files
    for file_name in os.listdir(path):
        if file_name.endswith('.json'):

            # open file
            with open(os.path.join(path, file_name)) as json_file:
                data = json.load(json_file)

                # search for key
                for k, v in data[category].items():
                    # add key
                    if not key in data[category][k]:

                        data[category][k][key] = eval(value)

                    else:
                        text = f"changing: {category},{k},{data[category][k][key]} to {eval(value)}:"
                        data[category][k][key] = eval(value)

                        print(text)

            write_file(file_name, folder, data)


def compare_json(default, data, file_name, path=""):
    for key in default:
        if key not in data:
            print(f"Key '{key}' is missing in {file_name} at path {path}")
        else:
            if isinstance(default[key], dict) and isinstance(data[key], dict):
                compare_json(default[key], data[key], file_name, path + f"['{key}']")
            # Check for exact match of nested dictionaries
            elif default[key] != data[key]:
                pass
                # print(f"Value of key '{key}' is changed from '{default[key]}' to '{data[key]}' in {file_name} at path {path}")


def abs_database_path():
    # gets the path to store the files: database at root
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_database_path_ = os.path.split(dir_path)[0].split("source")[0] + "database" + os.sep
    return abs_database_path_


def abs_level_path():
    return os.path.join(abs_database_path(), "levels")


def abs_games_path():
    return os.path.join(abs_database_path(), "games")


def abs_players_path():
    return os.path.join(abs_database_path(), "players")


# def write_file(filename, folder, data):
#     with open(os.path.join(abs_database_path() + folder + os.sep + filename), 'w') as file:
#         json.dump(data, file, indent=4, sort_keys=False)

import os
import json
import shutil
from datetime import datetime

def create_backup(file_path, backup_folder):
    """Create a backup of the file if it exists.
        called by write_file
    """
    if os.path.exists(file_path):
        # Ensure backup folder exists
        os.makedirs(backup_folder, exist_ok=True)

        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        backup_path = os.path.join(backup_folder, backup_filename)

        try:
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Failed to create backup: {e}")
    return None

def get_latest_backup(backup_folder, original_filename):
    """Get the path of the latest backup file.
        called by write_file"""
    base_name = os.path.splitext(original_filename)[0]
    backups = [f for f in os.listdir(backup_folder) if f.startswith(base_name) and f.endswith(os.path.splitext(original_filename)[1])]
    if backups:
        return os.path.join(backup_folder, max(backups))
    return None

def write_file(filename, folder, data):
    """Write data to a file, creating a backup if the file exists."""
    file_path = os.path.join(abs_database_path(), folder, filename)
    backup_folder = os.path.join(abs_database_path(), 'backups', folder)

    # Create backup
    create_backup(file_path, backup_folder)

    # Write the new data
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=False)
        print(f"File successfully written: {file_path}")
    except Exception as e:
        print(f"Failed to write file: {e}")
        # If writing fails, try to restore from the latest backup
        latest_backup = get_latest_backup(backup_folder, filename)
        if latest_backup:
            try:
                shutil.copy2(latest_backup, file_path)
                print(f"Restored from backup: {latest_backup}")
            except Exception as e:
                print(f"Failed to restore from backup: {e}")



def load_file(filename, folder):
    path = os.path.join(abs_database_path() + folder + os.sep + filename)
    try:
        with open(path, 'r+') as file:
            data = json.load(file)

    except FileNotFoundError:
        # # No save_load file, so create one
        # data = create_file(filename)
        # write_file(filename, data)
        print("load_file error: FileNotFoundError:", filename)
        data = None
    return data


def get_level_list():
    file_list = [file for file in os.listdir(abs_level_path()) if file.startswith("level_")]
    return file_list


def get_games_list():
    file_list = [file for file in os.listdir(abs_games_path())]
    # sort: oldest last
    file_list.sort(key=lambda x: os.path.getctime(os.path.join(abs_games_path(), x)), reverse=True)
    return file_list


def get_ships_list():
    file = load_file("ship_settings.json", "config")
    return file.keys()


def get_player_list():
    file = load_file("players.json", "config")
    # file_list = [file for file in os.listdir(abs_players_path()) if file.startswith("player_")]
    return len(file.keys())
    # return file_list


def generate_json_filename_based_on_datetime(prefix):
    current_datetime = datetime.datetime.now().strftime("%Y.%m.%d %Hh%Mm%Ss")
    return f"{prefix} {current_datetime}.json"


def move_file_to_trash(file_path):
    try:
        send2trash.send2trash(file_path)
        print(f"The file at {file_path} has been moved to the trash.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    pass
    # update_json_files(load_file("level_0.json", folder="levels"))
    compare_json_files(abs_level_path(), load_file("level_0.json", folder="levels"))
    # update_files("games", "ships", "owner", 0, None)
    # update_files("levels", "celestial_objects", "owner", 0, condition="data[category][k]['explored'] == True" )
    # update_files("levels", "celestial_objects", "owner", 1, condition="data[category][k]['alien_population'] > 0")
    # update_files("levels", "globals", "population_density", 50.0, condition=None)
    # compare_json_files(abs_level_path(), load_file("level_6.json", folder="levels_bk"))
    # update_files("levels", "celestial_objects", "buildings", [], condition="data[category][k]['buildings'] != []")
    # update_files("levels", "celestial_objects", "buildings", [], condition="data[category][k]['buildings'] != []")
    # update_level_files("levels", "ships", "energy_use", "data[category][k][key] / 10")


if __name__ == "__main__":
    main()
    # print (load_file("level_0.json", folder ="levels"))
    # tests
    # print ("os.path.join(os.getcwd(),settings.json", os.path.join(os.getcwd(),"settings.json"))
    # print("working dir: os.path.join(os.getcwd()) :", os.path.join(os.getcwd()))
    #
    # file_path = os.path.dirname(os.path.realpath(__file__))
    # print ("file_path = os.path.dirname(os.path.realpath(__file__)): ", file_path)
    # abs_root = os.path.split(file_path)[0]
    #
    # print ("abs_root = os.path.split(file_path)[0]:",abs_root )
    #
    #
    # print ("database:", abs_database_path())
