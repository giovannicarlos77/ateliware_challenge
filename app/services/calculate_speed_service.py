import requests


def fetch_speed_data():
    url = "https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch speed data")
