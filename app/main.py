from flask import Flask

from app.services.calculate_speed_service import fetch_speed_data
from app.services.drone_service import create_chessboard_graph
from app.api.routes import setup_routes

app = Flask(__name__)

# Get speed data
speed_data = fetch_speed_data()

# Create the chessboard graph
chessboard_graph, edge_weights = create_chessboard_graph(speed_data)

# Setup routes
setup_routes(app, chessboard_graph, edge_weights)

if __name__ == "__main__":
    app.run(debug=False)
