from flask import Flask
from app.services.drone_service import create_chessboard_graph
from app.api.routes import setup_routes

app = Flask(__name__)

# Create the chessboard graph
chessboard_graph = create_chessboard_graph()

# Setup routes
setup_routes(app, chessboard_graph)

if __name__ == "__main__":
    app.run(debug=False)
