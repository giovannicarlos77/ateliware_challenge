import pytest
import requests_mock

from app.services.calculate_speed_service import fetch_speed_data


def test_fetch_speed_data_success():
    # Setup the URL and the expected mock response
    url = "https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f"
    mock_data = {}

    # Use requests_mock to mock the response
    with requests_mock.Mocker() as m:
        m.get(url, json=mock_data, status_code=200)
        try:
            result = fetch_speed_data()
            assert result == mock_data
        except Exception:
            pytest.fail("fetch_speed_data() raised an exception unexpectedly!")


def test_fetch_speed_data_failure():
    # Setup the URL and the expected mock response for failure
    url = "https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f"

    # Use requests_mock to mock the response
    with requests_mock.Mocker() as m:
        m.get(url, status_code=500)
        with pytest.raises(Exception) as excinfo:
            fetch_speed_data()

        assert "Failed to fetch speed data" in str(excinfo.value)
