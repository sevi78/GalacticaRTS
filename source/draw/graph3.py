import json
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Load the JSON data
with open('C:\\Users\\sever\\Documents\\Galactica-RTS_zoomable1.107\\database\\config\\buildings.json', 'r') as file:
    data = json.load(file)

# Step 2: Create the Dependency Graph
G = nx.DiGraph()

# Add nodes with attributes
for category, buildings in data.items():
    for building, attributes in buildings.items():
        G.add_node(building, **attributes)

def show_production():
    # Add edges based on dependencies
    for category, buildings in data.items():
        for building, attributes in buildings.items():
            for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water', 'production_technology', 'production_population']:
                if attributes[resource] > 0:  # If a building produces a resource
                    for other_category, other_buildings in data.items():
                        for other_building, other_attributes in other_buildings.items():
                            if building != other_building and other_attributes[resource] < 0:  # If another building consumes that resource
                                G.add_edge(building, other_building, category=category)

def show_prices():
    # Add edges based on dependencies
    for category, buildings in data.items():
        for building, attributes in buildings.items():
            for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water', 'production_technology', 'production_population']:
                if attributes[resource] > 0:  # If a building produces a resource
                    for other_category, other_buildings in data.items():
                        for other_building, other_attributes in other_buildings.items():
                            if building != other_building and other_attributes[resource] < 0:  # If another building consumes that resource
                                G.add_edge(building, other_building, category=category)

show_production()
# Step 3: Plot the Dependency Graph with Circular Layout
pos = nx.circular_layout(G)
pos = nx.arf_layout(G)# positions for all nodes
pos = nx.bipartite_layout(G,G.nodes)
pos = nx.kamada_kawai_layout(G,G.nodes)

# Draw nodes
nx.draw_networkx_nodes(G, pos)

# Draw edges with labels
for edge in G.edges(data=True):
    nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], arrowstyle='->')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(edge[0], edge[1]): edge[2]['category']})

# Draw node labels
nx.draw_networkx_labels(G, pos)

plt.show()
