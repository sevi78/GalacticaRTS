import datetime
import glob
import os
import json

import send2trash

dirpath = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "pictures" + os.sep
gifs_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "gifs" + os.sep
soundpath = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "sounds" + os.sep



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


def abs_database_path():
    # gets the path to store the files: database at root
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_database_path = os.path.split(dir_path)[0].split("source")[0] + "database" + os.sep
    return abs_database_path

def abs_level_path():
    return (os.path.join(abs_database_path(), "levels" ))

def abs_games_path():
    return (os.path.join(abs_database_path(), "games" ))

def write_file(filename, data, **kwargs):
    folder = kwargs.get("folder", "")
    with open(os.path.join(abs_database_path() + folder  + os.sep + filename), 'w') as file:
        json.dump(data, file)

def load_file(filename, **kwargs):
    folder = kwargs.get("folder", "")
    path = os.path.join(abs_database_path() + folder  + os.sep +  filename)
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
    return file_list

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
    update_json_files(load_file("level_0.json", folder="levels"))


if __name__ == "__main__":
    main()
    #print (load_file("level_0.json", folder ="levels"))
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
