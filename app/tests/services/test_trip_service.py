from datetime import date
from unittest.mock import MagicMock
import pytest
from sqlalchemy.sql.elements import UnaryExpression

from app.services.trip_service import TripService
from app.model.trip_model import Trip


@pytest.fixture
def mock_session():
    # Create a mock session object
    return MagicMock()


def test_save_trip(mock_session):
    trip_service = TripService(mock_session)
    path = "A-B-C"
    speed = 100

    trip_service.save_trip(path, speed)

    # Ensure that a Trip instance is created and added to the session
    mock_session.add.assert_called_once()
    new_trip = mock_session.add.call_args[0][0]
    assert isinstance(new_trip, Trip)
    assert new_trip.path == path
    assert new_trip.speed == speed
    assert new_trip.date == date.today()

    # Ensure that the session is committed
    mock_session.commit.assert_called_once()


def test_get_last_10_trips(mock_session):
    trip_service = TripService(mock_session)

    mock_trips = [MagicMock(spec=Trip) for _ in range(10)]
    mock_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = mock_trips

    result = trip_service.get_last_10_trips()

    mock_session.query.assert_called_with(Trip)

    assert mock_session.query.return_value.order_by.called


def test_close(mock_session):
    trip_service = TripService(mock_session)

    trip_service.close()

    # Ensure that the session is closed
    mock_session.close.assert_called_once()
