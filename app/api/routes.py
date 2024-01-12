from flask import request, jsonify

from app.model.trip_model import session
from app.services.drone_service import dijkstra_full_path
from app.services.trip_service import TripService


def setup_routes(app, chessboard_graph, edge_weights):
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

        path, speed = dijkstra_full_path(chessboard_graph, start, pickup, end, edge_weights)
        if isinstance(path, str):
            return jsonify({"error": path}), 400

        trip_service = TripService(session)

        # Get last 10 trips
        last_10_trips = trip_service.get_last_10_trips()

        # Array to store trip details
        trip_details = []

        # Append trip details to the array
        for trip in last_10_trips:
            trip_details.append({
                "ID": trip.id,
                "Path": trip.path,
                "Speed": trip.speed,
                "Date": trip.date.strftime("%Y-%m-%d")
            })

        # Join the path elements into a single string
        path_str = "-".join(path)

        summary_json = {"path": path_str, "total_speed": speed}

        result_json = {"trip_details": summary_json, "last_10_trips": trip_details}

        return jsonify(result_json)

