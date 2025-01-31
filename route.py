import networkx as nx # type: ignore
import matplotlib.pyplot as plt
from collections import deque

# Create a graph representation of the city map
city_graph = nx.Graph()

# Add intersections (nodes) and roads (edges)
edges = [
    ("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"),
    ("D", "F"), ("E", "F"), ("F", "G"), ("E", "H"), ("H", "G")
]
city_graph.add_edges_from(edges)

# Fixed node positions for consistency
fixed_positions = {
    "A": (0, 3), "B": (1, 4), "C": (1, 2), "D": (2, 3),
    "E": (2, 1), "F": (3, 2), "G": (4, 2), "H": (3, 0)
}

# Bi-Directional BFS Implementation
def bidirectional_bfs(graph, start, goal):
    if start == goal:
        return [start]
    
    front_queue = deque([start])
    back_queue = deque([goal])
    
    front_visited = {start: None}
    back_visited = {goal: None}
    
    while front_queue and back_queue:
        if front_queue:
            front_current = front_queue.popleft()
            for neighbor in graph.neighbors(front_current):
                if neighbor not in front_visited:
                    front_visited[neighbor] = front_current
                    front_queue.append(neighbor)
                if neighbor in back_visited:
                    return construct_path(front_visited, back_visited, neighbor)
        
        if back_queue:
            back_current = back_queue.popleft()
            for neighbor in graph.neighbors(back_current):
                if neighbor not in back_visited:
                    back_visited[neighbor] = back_current
                    back_queue.append(neighbor)
                if neighbor in front_visited:
                    return construct_path(front_visited, back_visited, neighbor)
    
    return None  # No path found

# Construct path from visited nodes
def construct_path(front_visited, back_visited, meeting_point):
    path = []
    
    node = meeting_point
    while node is not None:
        path.append(node)
        node = front_visited[node]
    
    path.reverse()
    
    node = back_visited[meeting_point]
    while node is not None:
        path.append(node)
        node = back_visited[node]
    
    return path

# Test the implementation
start_node = "A"
goal_node = "G"
shortest_path = bidirectional_bfs(city_graph, start_node, goal_node)

print("Shortest Path using Bi-Directional BFS:", shortest_path)

# Visualization using a fixed layout
plt.figure(figsize=(8, 6))
nx.draw(city_graph, fixed_positions, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(city_graph, fixed_positions, edgelist=path_edges, edge_color='red', width=2)
plt.title("City Map with Shortest Path")
plt.show()
