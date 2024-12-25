# from source.handlers.file_handler import load_file
#
# buildings = load_file("buildings.json", "config")
#
#
# def get_needed_buildings(building_name, buildings, population=0):
#     needed_buildings = []
#
#     # Find the building in the dictionary
#     building = None
#     for category_buildings in buildings.values():
#         if building_name in category_buildings:
#             building = category_buildings[building_name]
#             break
#
#     if not building:
#         return []  # Return an empty list if the building is not found
#
#     # Determine which resources are needed based on negative production values
#     for production_key, production_value in building.items():
#         if production_key.startswith('production_') and production_value < 0:
#             resource = production_key.split('_')[1]  # Extract resource type
#             needed_amount = -production_value
#             producers = find_producers(resource, needed_amount, buildings, population)
#             needed_buildings.extend(producers)
#
#     return needed_buildings
#
#
# def find_producers(resource, needed_amount, buildings, population):
#     producers = []
#     total_produced = 0
#
#     for category_buildings in buildings.values():
#         for building_name, building in category_buildings.items():
#             production_rate = building.get(f'production_{resource}', 0)
#             # Check if the building produces the needed resource and if population requirement is met
#             if production_rate > 0 and population >= building['build_population_minimum']:
#                 # Calculate how many of this building type are needed
#                 num_buildings = (needed_amount - total_produced + production_rate - 1) // production_rate
#                 producers.extend([building_name] * num_buildings)
#                 total_produced += production_rate * num_buildings
#
#                 # Stop adding more producers once the needed amount is met
#                 if total_produced >= needed_amount:
#                     break
#         if total_produced >= needed_amount:
#             break
#
#     return producers
#
#
# if __name__ == "__main__":
#     for category, category_buildings in buildings.items():
#         for building_name in category_buildings:
#             needed_for_building = get_needed_buildings(building_name, buildings, population=10000)
#             print(f"Buildings needed to construct {building_name}: {needed_for_building}")
#
# from source.handlers.file_handler import load_file
#
# buildings = load_file("buildings.json", "config")
#
# def get_needed_buildings_recursively(building_name, buildings, population=0, visited=None):
#     if visited is None:
#         visited = set()
#
#     needed_buildings = []
#
#     # Find the building in the dictionary
#     building = None
#     for category_buildings in buildings.values():
#         if building_name in category_buildings:
#             building = category_buildings[building_name]
#             break
#
#     if not building:
#         return []  # Return an empty list if the building is not found
#
#     # Prevent infinite recursion by checking if the building has already been visited
#     if building_name in visited:
#         return []
#
#     # Mark the building as visited
#     visited.add(building_name)
#
#     # Determine which resources are needed based on negative production values
#     for production_key, production_value in building.items():
#         if production_key.startswith('production_') and production_value < 0:
#             resource = production_key.split('_')[1]  # Extract resource type
#             needed_amount = -production_value
#             producers = find_producers(resource, needed_amount, buildings, population)
#
#             for producer_name in producers:
#                 needed_buildings.append(producer_name)
#                 # Recursively find what is needed to produce the producer
#                 needed_buildings.extend(get_needed_buildings_recursively(producer_name, buildings, population, visited))
#
#     return needed_buildings
#
# def find_producers(resource, needed_amount, buildings, population):
#     producers = []
#     total_produced = 0
#
#     for category_buildings in buildings.values():
#         for building_name, building in category_buildings.items():
#             production_rate = building.get(f'production_{resource}', 0)
#             # Check if the building produces the needed resource and if population requirement is met
#             if production_rate > 0 and population >= building['build_population_minimum']:
#                 # Calculate how many of this building type are needed
#                 num_buildings = (needed_amount - total_produced + production_rate - 1) // production_rate
#                 producers.extend([building_name] * num_buildings)
#                 total_produced += production_rate * num_buildings
#
#                 # Stop adding more producers once the needed amount is met
#                 if total_produced >= needed_amount:
#                     break
#         if total_produced >= needed_amount:
#             break
#
#     return producers
#
# if __name__ == "__main__":
#     for category, category_buildings in buildings.items():
#         for building_name in category_buildings:
#             needed_for_building = get_needed_buildings_recursively(building_name, buildings, population=10000)
#             print(f"Buildings needed to construct {building_name}: {needed_for_building}")
#
from source.handlers.file_handler import load_file

buildings = load_file("buildings.json", "config")

def get_needed_buildings_recursively(building_name, buildings, population=0, visited=None):
    if visited is None:
        visited = set()

    needed_buildings = []

    # Find the building in the dictionary
    building = None
    for category_buildings in buildings.values():
        if building_name in category_buildings:
            building = category_buildings[building_name]
            break

    if not building or building_name in visited:
        return []  # Return an empty list if the building is not found or already visited

    # Check if the population is sufficient to build this building
    if population < building['build_population_minimum']:
        return []

    # Mark the building as visited
    visited.add(building_name)

    # Determine which resources are needed based on negative production values
    for production_key, production_value in building.items():
        if production_key.startswith('production_') and production_value < 0:
            resource = production_key.split('_')[1]  # Extract resource type
            needed_amount = -production_value
            producers = find_producers(resource, needed_amount, buildings, population)

            for producer_name in producers:
                needed_buildings.append(producer_name)
                # Recursively find what is needed to produce the producer
                needed_buildings.extend(get_needed_buildings_recursively(producer_name, buildings, population, visited))

    return needed_buildings

def find_producers(resource, needed_amount, buildings, population):
    producers = []
    total_produced = 0

    for category, category_buildings in buildings.items():
        selected_building = None
        for building_name, building in category_buildings.items():
            production_rate = building.get(f'production_{resource}', 0)
            # Select the appropriate building based on population
            if production_rate > 0 and population >= building['build_population_minimum']:
                if population < 1000 and building['build_population_minimum'] == 0:
                    selected_building = building
                elif 1000 <= population < 10000 and building['build_population_minimum'] <= 1000:
                    selected_building = building
                elif population >= 10000 and building['build_population_minimum'] <= 10000:
                    selected_building = building

        if selected_building:
            production_rate = selected_building.get(f'production_{resource}', 0)
            if production_rate > 0:
                num_buildings = (needed_amount - total_produced + production_rate - 1) // production_rate
                producers.extend([selected_building['name']] * num_buildings)
                total_produced += production_rate * num_buildings

                if total_produced >= needed_amount:
                    break

    return producers

if __name__ == "__main__":
    for category, category_buildings in buildings.items():
        for building_name in category_buildings:
            needed_for_building = get_needed_buildings_recursively(building_name, buildings, population=1000)
            print(f"Buildings needed to construct {building_name}: {needed_for_building}")



