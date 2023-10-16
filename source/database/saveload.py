import json
import os


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

#
# if __name__ == "__main__":
#
#     # tests
#     print ("os.path.join(os.getcwd(),settings.json", os.path.join(os.getcwd(),"settings.json"))
#     print("working dir: os.path.join(os.getcwd()) :", os.path.join(os.getcwd()))
#
#     file_path = os.path.dirname(os.path.realpath(__file__))
#     print ("file_path = os.path.dirname(os.path.realpath(__file__)): ", file_path)
#     abs_root = os.path.split(file_path)[0]
#
#     print ("abs_root = os.path.split(file_path)[0]:",abs_root )
#
#
#     print ("database:", abs_database())
