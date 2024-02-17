# import json
# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Step 1: Load the JSON data
# with open('C:\\Users\\sever\\Documents\\Galactica-RTS_zoomable1.107\\database\\config\\buildings.json', 'r') as file:
#     data = json.load(file)
#
# # Step 2: Create the Dependency Graph
# G = nx.DiGraph()
#
# # Add nodes with attributes
# for category, buildings in data.items():
#     for building, attributes in buildings.items():
#         G.add_node(building, **attributes)
#
# # Add edges based on dependencies
# for category, buildings in data.items():
#     for building, attributes in buildings.items():
#         for other_category, other_buildings in data.items():
#             for other_building, other_attributes in other_buildings.items():
#                 if building != other_building:  # Avoid self-loops
#                     # If a building produces something that another consumes
#                     for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water', 'production_technology', 'production_population']:
#                         if attributes[resource] > 0 and other_attributes[resource] < 0:
#                             G.add_edge(building, other_building, category=other_category)
#
# # Step 3: Plot the Dependency Graph
# pos = nx.spring_layout(G)  # positions for all nodes
#
# # Draw nodes
# nx.draw_networkx_nodes(G, pos)
#
# # Draw edges with labels
# for edge in G.edges(data=True):
#     nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], arrowstyle='->')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels={(edge[0], edge[1]): edge[2]['category']})
#
# # Draw node labels
# nx.draw_networkx_labels(G, pos)
#
# plt.show()


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
        for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water',
                         'production_technology', 'production_population']:
            if attributes[resource] > 0:  # If a building produces a resource
                for other_category, other_buildings in data.items():
                    for other_building, other_attributes in other_buildings.items():
                        if building != other_building and other_attributes[
                            resource] < 0:  # If another building consumes that resource
                            G.add_edge(building, other_building, category=category)

# Step 3: Plot the Dependency Graph
pos = nx.spring_layout(G)  # positions for all nodes

# Draw nodes
nx.draw_networkx_nodes(G, pos)

# Draw edges with labels
for edge in G.edges(data=True):
    nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], arrowstyle='->')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(edge[0], edge[1]): edge[2]['category']})

# Draw node labels
nx.draw_networkx_labels(G, pos)

plt.show()
