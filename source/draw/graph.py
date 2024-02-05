import json

import matplotlib.pyplot as plt
import networkx as nx

# Step 1: Load the JSON data
with open('C:\\Users\\sever\\Documents\\Galactica-RTS_zoomable1.107\\database\\config\\buildings.json', 'r') as file:
    data = json.load(file)

# Step 2: Create the Dependency Graph
G = nx.DiGraph()

# Add nodes with attributes
for category, buildings in data.items():
    for building, attributes in buildings.items():
        G.add_node(building, **attributes)

# Add edges based on dependencies
for category, buildings in data.items():
    for building, attributes in buildings.items():
        for other_category, other_buildings in data.items():
            for other_building, other_attributes in other_buildings.items():
                if building != other_building:  # Avoid self-loops
                    # If a building produces something that another consumes
                    for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water', 'production_technology', 'production_population']:
                        if attributes[resource] > 0 and other_attributes[resource] < 0:
                            G.add_edge(building, other_building)

# Step 3: Plot the Dependency Graph
# pos = nx.spring_layout(G)  # positions for all nodes
# nx.draw(G, pos, with_labels=True, node_size=500)
# plt.show()
#
# pos = nx.shell_layout(G)
# nx.draw(G, pos, with_labels=True, node_size=500)
# plt.show()
#
# pos = nx.random_layout(G)
# nx.draw(G, pos, with_labels=True, node_size=500)
# plt.show()
#
# pos = nx.circular_layout(G)
# nx.draw(G, pos, with_labels=True, node_size=500)
# plt.show()
#
# pos = nx.fruchterman_reingold_layout(G)
# nx.draw(G, pos, with_labels=True, node_size=500)
# plt.show()

pos = nx.arf_layout(G)
nx.draw(G, pos, with_labels=True, node_size=500)
plt.show()
