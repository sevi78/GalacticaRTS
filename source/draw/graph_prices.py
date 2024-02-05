# import json
# import networkx as nx
# import matplotlib.pyplot as plt
# import ipywidgets as widgets
# from IPython.display import display
#
# # Step 1: Load the JSON data
# with open(r'C:\\Users\\sever\\Documents\\Galactica-RTS_zoomable1.107\\database\\config\\buildings.json', 'r') as file:
#     data = json.load(file)
#
# # Step 2: Create the Dependency Graph
# G = nx.DiGraph()
#
# # Add nodes for categories
#
#
#
# # Add nodes for buildings and edges to categories
# for category, buildings in data.items():
#     G.add_node(category, type='category')
#     for building, attributes in buildings.items():
#         G.add_node(building, type='building')
#         for resource, value in attributes.items():
#             if resource.startswith('price_') and value > 0:
#                 G.add_edge(building, resource[6:])
#
# # Create an interactive plot
# def plot_graph():
#     plt.figure(figsize=(10, 10))
#     pos = nx.spring_layout(G)  # positions for all nodes
#     pos = nx.kamada_kawai_layout(G, G.nodes)
#     pos = nx.spectral_layout(G)
#     pos = nx.spiral_layout(G)
#
#
#     # Draw nodes
#     building_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'building']
#     category_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'category']
#     nx.draw_networkx_nodes(G, pos, nodelist=building_nodes, node_color='skyblue', node_size=100)
#     nx.draw_networkx_nodes(G, pos, nodelist=category_nodes, node_color='lightgreen', node_size=500)
#
#     # Draw edges
#     nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
#
#     # Draw labels
#     labels = {node: node if data['type'] == 'building' else '' for node, data in G.nodes(data=True)}
#     nx.draw_networkx_labels(G, pos, labels=labels)
#
#     labels = {node: node if data['type'] == 'category' else '' for node, data in G.nodes(data=True)}
#     nx.draw_networkx_labels(G, pos, labels=labels)
#
#     plt.axis('off')
#     plt.show()
#
# # Display the interactive plot
# plot_graph()
#

import json
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Load the JSON data
with open(r'C:\\Users\\sever\\Documents\\Galactica-RTS_zoomable1.107\\database\\config\\buildings.json', 'r') as file:
    data = json.load(file)

# Step 2: Create the Dependency Graph
G = nx.DiGraph()


def show_prices():

    # Add nodes for buildings and edges to categories
    for category, buildings in data.items():
        # Add nodes for categories
        G.add_node(category, type='category')

        # add nodes for buildings
        for building, attributes in buildings.items():
            G.add_node(building, type='building', category=category)  # Add the category as an attribute
            for resource, value in attributes.items():
                if resource.startswith('price_') and value > 0:
                    G.add_edge(building, resource[6:], weight=value)  # Use the price as the weight of the edge


def show_production():
    # Add edges based on dependencies
    for category, buildings in data.items():
        # Add nodes for categories
        G.add_node(category, type='category')

        # add nodes for buildings
        for building, attributes in buildings.items():
            G.add_node(building, type='building', category=category)  # Add the category as an attribute
            for resource in ['production_energy', 'production_food', 'production_minerals', 'production_water', 'production_technology', 'production_population']:
                if attributes[resource] > 0:  # If a building produces a resource
                    for other_category, other_buildings in data.items():
                        for other_building, other_attributes in other_buildings.items():
                            if building != other_building and other_attributes[resource] < 0:  # If another building consumes that resource
                                G.add_edge(building, other_building, category=category)

#show_prices()
show_production()

# Create an interactive plot
def plot_graph():
    plt.figure(figsize=(15, 15))

    # Define the layout
    pos = {}
    categories = list(data.keys())
    for i, category in enumerate(categories):
        pos[category] = (i, 0)  # Categories are aligned horizontally at the bottom
        building_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'building' and data['category'] == category]
        for j, building in enumerate(building_nodes):
            pos[building] = (i, j+1)  # Other nodes are positioned above their category

    # Draw nodes
    building_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'building']
    category_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'category']
    nx.draw_networkx_nodes(G, pos, nodelist=building_nodes, node_color='skyblue', node_size=600)
    nx.draw_networkx_nodes(G, pos, nodelist=category_nodes, node_color='lightgreen', node_size=1000)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')

    # Draw labels
    labels = {node: node for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=labels)

    plt.axis('on')
    plt.show()

# Display the interactive plot
plot_graph()


