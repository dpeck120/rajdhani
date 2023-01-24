"""
Module to interact with the database.
"""

from . import placeholders
from . import db_ops

db_ops.ensure_db()

# config has 'db_uri' that can be used to connect to the database
from . import config

ticket_classes = {
            "SL":"sleeper",
            "3A":"third_ac",
            "2A":"second_ac",
            "1A":"first_ac",
            "FC":"first_class",
            "CC":"chair_car"
        }

def search_trains(
        from_station_code,
        to_station_code,
        ticket_class=None,
        departure_date=None,
        departure_time=[],
        arrival_time=[]):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """
    
    q = f"""select
            number,
            name,
            from_station_code,
            from_station_name,
            to_station_code,
            to_station_name,
            departure,
            arrival,
            duration_h,
            duration_m
            from train
            where from_station_code == '{from_station_code}'
            and to_station_code == '{to_station_code}'
        """

    if ticket_class in ticket_classes:
        q += f"and {ticket_classes[ticket_class]} == true"

    columns, rows = db_ops.exec_query(q)

    results = []

    for row in rows:
        results.append(dict(zip(columns,row)))

    return results

def search_stations(q):
    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """
    # TODO: make a db query to get the matching stations
    # and replace the following dummy implementation
    return placeholders.AUTOCOMPLETE_STATIONS

def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    return placeholders.SCHEDULE

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    # TODO: make a db query and insert a new booking
    # into the booking table

    return placeholders.TRIPS[0]

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    return placeholders.TRIPS
