import pytest
from unittest.mock import MagicMock, patch
from app.services.drone_service import create_chessboard_graph, dijkstra, dijkstra_full_path, TripService


@pytest.fixture
def mock_session():
    return MagicMock()


def test_create_chessboard_graph():
    graph, edge_weights = create_chessboard_graph()
    assert 'A1' in graph.edges and 'A2' in graph.edges['A1']


def test_dijkstra():
    graph, edge_weights = create_chessboard_graph()
    path, speed = dijkstra(graph, 'A1', 'A3', edge_weights)
    assert path == ['A1', 'A2', 'A3']
    assert speed == 2.0  # Assuming default weights of 1.0


@patch('app.services.trip_service.TripService')
def test_dijkstra_full_path(MockTripService, mock_session):
    graph, edge_weights = create_chessboard_graph()

    # Set up the mock TripService instance
    mock_trip_service = MockTripService.return_value
    mock_trip_service.save_trip = MagicMock()

    path, speed = dijkstra_full_path(graph, 'A1', 'A3', 'A4', edge_weights)

    assert path == ['A1', 'A2', 'A3', 'A4']
    assert speed == 3.0
