from pprint import pprint

from source.factories.building_factory import building_factory

buildings = building_factory.get_json_dict()
def main():

    pprint (buildings)

if __name__ == "__main__":
    main()
