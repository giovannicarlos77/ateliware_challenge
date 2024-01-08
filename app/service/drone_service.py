class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node in self.edges:
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = [to_node]

        if to_node in self.edges:
            self.edges[to_node].append(from_node)
        else:
            self.edges[to_node] = [from_node]

        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


def create_chessboard_graph():
    chessboard = Graph()
    rows = "ABCDEFGH"
    for row in rows:
        for col in range(1, 9):
            node = f"{row}{col}"
            if row != 'H':
                chessboard.add_edge(node, f"{chr(ord(row) + 1)}{col}", 1)
            if col != 8:
                chessboard.add_edge(node, f"{row}{col + 1}", 1)
    return chessboard


def dijkstra(graph, start, end):
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    path = path[::-1]
    return path
