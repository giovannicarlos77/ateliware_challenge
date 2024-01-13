
# Chessboard Drone Pathfinding Service

## Introduction

This project, developed as a challenge by Ateliware, focuses on optimizing drone delivery services using pathfinding algorithms. The application simulates efficient drone movements across a grid-like structure, similar to a chessboard, to determine the shortest delivery routes.

## Challenges

Implementing the project involved conceptualizing the chessboard as a graph and applying graph theory in Python. The adapted graph-based solution addresses the unique movement constraints of a drone navigating a chessboard layout.

## API Usage

### Making API Calls

To request a route calculation, send a JSON request to the following URL:

```
http://localhost:5000/api/calculate-route
```

#### Request Example

```json
{
    "start": "D1",
    "pickup": "D4",
    "end": "G8"
}
```

#### Response Example

The API responds with the details of the last 10 trips and the current trip:

```json
{
    "last_10_trips": [
        {
            "Date": "2024-01-12",
            "ID": 1,
            "Path": "D1-D2-D3-D4-E4-E5-E6-E7-E8-F8-G8",
            "Speed": 232.20000000000002
        }
    ],
    "trip_details": {
        "path": "D1-D2-D3-D4-E4-E5-E6-E7-E8-F8-G8",
        "total_speed": 232.20000000000002
    }
}
```

## Technologies Used

- Flask
- SQLAlchemy
- Pytest

## How to Use the Project

### Local Setup

1. Ensure Python and Pipenv are installed on your system.
2. Navigate to the root directory of the project and run `pipenv install` to install dependencies.
3. Activate the virtual environment with `pipenv shell`.

### Running the Application

1. After activating the virtual environment, run the application from the root directory of the project using:
   ```bash
   flask --app main.py run
   ```
2. Access the application at `http://localhost:5000`.

### Using Docker

1. Install Docker on your system.
2. Build the Docker container in the project root directory:
   ```bash
   docker build -t chessboard-drone-pathfinder .
   ```
3. Run the container:
   ```bash
   docker run -p 5000:5000 chessboard-drone-pathfinder
   ```
