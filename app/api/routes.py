from flask import request, jsonify
from app.services.drone_service import dijkstra_full_path


def setup_routes(app, chessboard_graph):
    @app.route('/api/calculate-route', methods=['POST'])
    def calculate_route():
        data = request.json

        # Validate the existence of input data
        if not data or 'start' not in data or 'pickup' not in data or 'end' not in data:
            return jsonify({"error": "Please provide start, pickup, and end points."}), 400

        start = data.get('start')
        pickup = data.get('pickup')
        end = data.get('end')

        # Validate the format of the chessboard coordinates (e.g., A1, H8)
        if not (len(start) == len(pickup) == len(end) == 2):
            return jsonify({"error": "Each point must be exactly two characters long."}), 400

        valid_letters = "ABCDEFGH"
        valid_numbers = "12345678"
        for point in [start, pickup, end]:
            if point[0] not in valid_letters or point[1] not in valid_numbers:
                return jsonify({"error": f"Invalid chessboard point: {point}"}), 400

        path = dijkstra_full_path(chessboard_graph, start, pickup, end)
        if isinstance(path, str):
            return jsonify({"error": path}), 400

        # Join the path elements into a single string
        path_str = " -> ".join(path)
        return jsonify({"path": path_str})

