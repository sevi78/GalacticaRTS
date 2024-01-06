import glob
import os
import json

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


def update_json_files(keyword, default_dict):
    # Full path to the 'database' directory
    path = '/database'

    # Use os.path.join to create the full path to the .json files
    full_path = os.path.join(path, '*.json')

    # Iterate over all .json files in the 'database' directory
    for filename in glob.glob(full_path):
        # Check if filename starts with the keyword
        if os.path.basename(filename).startswith(keyword):
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


def abs_database():
    # gets the path to store the files: database at root
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_database_path = os.path.split(dir_path)[0].split("source")[0] + "database" + os.sep
    return abs_database_path


def load_existing_file(filename):
    with open(os.path.join(abs_database() + filename), 'r+') as file:
        file = json.load(file)
    return file


def write_file(filename, data):
    with open(os.path.join(abs_database() + filename), 'w') as file:
        json.dump(data, file)


def load_file(filename):
    try:
        # Save is loaded
        data = load_existing_file(filename)
    except FileNotFoundError:
        # # No save_load file, so create one
        # data = create_file(filename)
        # write_file(filename, data)
        print("load_file error: FileNotFoundError:", filename)
        data = None
    return data


def get_level_list():
    """
    Get a list of all files in the database directory which starts with "level_".

    Parameters:
    database_directory (str): The path to the database directory.

    Returns:
    list: A list of filenames that start with "level_".
    """

    database_path = abs_database()
    file_list = [file for file in os.listdir(database_path) if file.startswith("level_")]
    return file_list


def main():
    pass
    # update_json_files("level_", load_file("level_0.json"))


if __name__ == "__main__":
    main()

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
    # print ("database:", abs_database())
