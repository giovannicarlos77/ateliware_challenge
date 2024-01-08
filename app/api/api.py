from flask import request, jsonify
from ..service.drone_service import dijkstra


def setup_routes(app, chessboard_graph):
    @app.route('/route', methods=['POST'])
    def calculate_route():
        data = request.json
        start = data.get('start')
        end = data.get('end')
        path = dijkstra(chessboard_graph, start, end)
        return jsonify({"path": path})
