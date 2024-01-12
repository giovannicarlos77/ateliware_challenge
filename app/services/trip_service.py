from datetime import date

from app.model.trip_model import Trip


class TripService:
    def __init__(self, session):
        self.session = session

    def save_trip(self, path, speed):
        new_trip = Trip(path=path, speed=speed, date=date.today())
        self.session.add(new_trip)
        self.session.commit()

    def get_last_10_trips(self):
        trips = self.session.query(Trip).order_by(Trip.date.desc()).limit(10).all()
        return trips

    def close(self):
        self.session.close()