import datetime
import glob
import json
import os

import send2trash

dirpath = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "pictures" + os.sep
gifs_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "gifs" + os.sep
soundpath = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "sounds" + os.sep

"""TODO: 
fix write_file/load_file for make more consitency:
write_file(folder, filename, data)
load_file(folder, filename)
"""
def update_dict__(data, default_dict):
    for key, value in default_dict.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict):
            update_dict(data[key], value)


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


# def compare_json_files(folder, default_file):
#     for file_name in os.listdir(folder):
#         if file_name.endswith('.json'):
#             with open(os.path.join(folder, file_name)) as json_file:
#                 data = json.load(json_file)
#                 print(f"Comparing file: {file_name}")
#                 compare_json(default_file, data, file_name)
#
# def compare_json(default, data, file_name):
#     # Check for keys in data that are not in default
#     for key in data:
#         if key not in default:
#             print(f"Key '{key}' with value '{data[key]}' is not in default_file in {file_name}")
#
#     # Check for keys in default that are not in data
#     for key in default:
#         if key not in data:
#             print(f"Key '{key}' is missing in {file_name}")
# def compare_json_files(folder, default_file):
#     for file_name in os.listdir(folder):
#         if file_name.endswith('.json'):
#             with open(os.path.join(folder, file_name)) as json_file:
#                 data = json.load(json_file)
#                 print(f"Comparing file: {file_name}")
#                 compare_json(default_file, data, file_name)
#
# def compare_json(default, data, file_name, path=""):
#     for key in default:
#         if key not in data:
#             print(f"Key '{key}' is missing in {file_name} at path {path}")
#         else:
#             if isinstance(default[key], dict) and isinstance(data[key], dict):
#                 compare_json(default[key], data[key], file_name, path + f"['{key}']")
#             elif default[key] != data[key]:
#                 print(f"Value of key '{key}' is changed from '{default[key]}' to '{data[key]}' in {file_name} at path {path}")

def compare_json_files(folder, default_file):
    for file_name in os.listdir(folder):
        if file_name.endswith('.json'):
            with open(os.path.join(folder, file_name)) as json_file:
                data = json.load(json_file)
                print(f"Comparing file: {file_name}")
                compare_json(default_file, data, file_name)

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
                #print(f"Value of key '{key}' is changed from '{default[key]}' to '{data[key]}' in {file_name} at path {path}")
def abs_database_path():
    # gets the path to store the files: database at root
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_database_path = os.path.split(dir_path)[0].split("source")[0] + "database" + os.sep
    return abs_database_path


def abs_level_path():
    return (os.path.join(abs_database_path(), "levels"))


def abs_games_path():
    return (os.path.join(abs_database_path(), "games"))


def write_file(filename, folder, data):
    with open(os.path.join(abs_database_path() + folder + os.sep + filename), 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


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
    #update_json_files(load_file("level_0.json", folder="levels"))
    compare_json_files(abs_level_path(),load_file("level_0.json", folder="levels"))


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