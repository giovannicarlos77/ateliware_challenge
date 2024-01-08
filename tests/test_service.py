
import pytest
from app.service import dijkstra, create_chessboard_graph

def test_dijkstra():
    chessboard = create_chessboard_graph()
    assert dijkstra(chessboard, 'A1', 'B2') == ['A1', 'B2']
    assert dijkstra(chessboard, 'A1', 'H8') == ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']
    assert dijkstra(chessboard, 'H8', 'A1') == ['H8', 'G8', 'F8', 'E8', 'D8', 'C8', 'B8', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2', 'A1']
    assert dijkstra(chessboard, 'D4', 'D4') == ['D4']
    assert dijkstra(chessboard, 'A1', 'I9') == 'Route Not Possible'
