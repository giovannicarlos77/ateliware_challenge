from app.model.trip_model import session
from app.services.trip_service import TripService


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.edges:
            self.edges[node1] = {}
        if node2 not in self.edges:
            self.edges[node2] = {}
        self.edges[node1][node2] = weight
        self.edges[node2][node1] = weight


def create_chessboard_graph(weights=None):
    chessboard = Graph()
    rows = "ABCDEFGH"

    # Create a dictionary to store edge weights
    edge_weights = {}

    for row in rows:
        for col in range(1, 9):
            node = f"{row}{col}"
            if col < 8:  # Add edge to the right
                target_node = f"{row}{col + 1}"
                weight = 1.0  # Default weight if not provided
                if weights and node in weights and target_node in weights[node]:
                    weight = weights[node][target_node]
                chessboard.add_edge(node, target_node, weight)
                edge_weights[(node, target_node)] = weight
                edge_weights[(target_node, node)] = weight
            if col > 1:  # Add edge to the left
                target_node = f"{row}{col - 1}"
                weight = 1.0  # Default weight if not provided
                if weights and node in weights and target_node in weights[node]:
                    weight = weights[node][target_node]
                chessboard.add_edge(node, target_node, weight)
                edge_weights[(node, target_node)] = weight
                edge_weights[(target_node, node)] = weight
            if row != 'H':  # Add edge upwards
                target_node = f"{chr(ord(row) + 1)}{col}"
                weight = 1.0  # Default weight if not provided
                if weights and node in weights and target_node in weights[node]:
                    weight = weights[node][target_node]
                chessboard.add_edge(node, target_node, weight)
                edge_weights[(node, target_node)] = weight
                edge_weights[(target_node, node)] = weight
            if row != 'A':  # Add edge downwards
                target_node = f"{chr(ord(row) - 1)}{col}"
                weight = 1.0  # Default weight if not provided
                if weights and node in weights and target_node in weights[node]:
                    weight = weights[node][target_node]
                chessboard.add_edge(node, target_node, weight)
                edge_weights[(node, target_node)] = weight
                edge_weights[(target_node, node)] = weight

    return chessboard, edge_weights


def dijkstra(graph, start, end, edge_weights):
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            if abs(ord(current_node[0]) - ord(next_node[0])) + abs(int(current_node[1]) - int(next_node[1])) != 1:
                continue  # Skip invalid moves

            if (current_node, next_node) in edge_weights:
                weight = edge_weights[(current_node, next_node)] + weight_to_current_node
            else:
                weight = 0  # Default weight for unweighted edges

            if next_node not in shortest_paths or weight < shortest_paths[next_node][1]:
                shortest_paths[next_node] = (current_node, weight)

        # Check for no valid path
        unvisited_nodes = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not unvisited_nodes:
            return None, None  # No path found

        current_node = min(unvisited_nodes, key=lambda k: unvisited_nodes[k][1])

    path = []
    current_speed = 0.0

    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        if next_node is not None:
            current_speed += edge_weights.get((current_node, next_node), 0.0)
        current_node = next_node

    path = path[::-1]

    return path, current_speed


def dijkstra_full_path(graph, start, pickup, delivery, edge_weights):
    trip_service = TripService(session)

    # Find the shortest path from start to pickup
    path_start_to_pickup, speed_start_to_pickup = dijkstra(graph, start, pickup, edge_weights)

    # If the route is not possible, return
    if path_start_to_pickup == "Route Not Possible":
        return "Route from start to pickup is not possible"

    # Find the shortest path from pickup to delivery
    path_pickup_to_delivery, speed_pickup_to_delivery = dijkstra(graph, pickup, delivery, edge_weights)

    # If the route is not possible, return
    if path_pickup_to_delivery == "Route Not Possible":
        return "Route from pickup to delivery is not possible"

    # Combine the two paths, excluding the duplicate pickup node
    full_path = path_start_to_pickup + path_pickup_to_delivery[1:]
    total_speed = speed_pickup_to_delivery + speed_pickup_to_delivery

    path_str = "-".join(full_path)
    trip_service.save_trip(path_str, total_speed)

    return full_path, total_speed
