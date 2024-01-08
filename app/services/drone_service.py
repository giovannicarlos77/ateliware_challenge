class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node in self.edges:
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = [to_node]

        self.weights[(from_node, to_node)] = weight


def create_chessboard_graph():
    chessboard = Graph()
    rows = "ABCDEFGH"
    for row in rows:
        for col in range(1, 9):
            node = f"{row}{col}"
            if col < 8:  # Add edge to the right
                chessboard.add_edge(node, f"{row}{col + 1}", 1)
            if col > 1:  # Add edge to the left
                chessboard.add_edge(node, f"{row}{col - 1}", 1)
            if row != 'H':  # Add edge upwards
                chessboard.add_edge(node, f"{chr(ord(row) + 1)}{col}", 1)
            if row != 'A':  # Add edge downwards
                chessboard.add_edge(node, f"{chr(ord(row) - 1)}{col}", 1)
    return chessboard


def dijkstra(graph, start, end, speed):
    # Assume speed is given in nodes per unit time. Distance between nodes is 1.
    # Time to travel between nodes is therefore 1/speed.

    if speed <= 0:
        return "Invalid speed. Speed must be greater than zero."

    shortest_paths = {start: (None, 0)}  # (Previous node, total time)
    current_node = start
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        time_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            time = 1 / speed + time_to_current_node  # Time to travel to next node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, time)
            else:
                current_shortest_time = shortest_paths[next_node][1]
                if current_shortest_time > time:
                    shortest_paths[next_node] = (current_node, time)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    total_time = 0
    while current_node is not None:
        path.append(current_node)
        next_node, time = shortest_paths[current_node]
        if next_node:
            total_time = time  # Update total time when moving to the previous node
        current_node = next_node
    path = path[::-1]

    return path


def dijkstra_full_path(graph, start, pickup, delivery):
    # Find the shortest path from start to pickup
    path_start_to_pickup = dijkstra(graph, start, pickup, 0.5)

    # If the route is not possible, return
    if path_start_to_pickup == "Route Not Possible":
        return "Route from start to pickup is not possible"

    # Find the shortest path from pickup to delivery
    path_pickup_to_delivery = dijkstra(graph, pickup, delivery, 0.5)

    # If the route is not possible, return
    if path_pickup_to_delivery == "Route Not Possible":
        return "Route from pickup to delivery is not possible"

    # Combine the two paths, excluding the duplicate pickup node
    full_path = path_start_to_pickup + path_pickup_to_delivery[1:]

    return full_path
