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

time_slots = {
    "slot1": (0,28800),
    "slot2": (28800,43200),
    "slot3": (43200,57600),
    "slot4": (57600,72000),
    "slot5": (72000,86400)
}

def get_time_query(slots, type):
    query = "and ("
    for slot in slots:
        query += f"({type} >= {time_slots[slot][0]} and {type} <= {time_slots[slot][1]}) or "

    query = f"{query[0:len(query)-3]})"

    return query

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

    query = f"""select
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
        query += f"and {ticket_classes[ticket_class]} == true "

    if len(departure_time) > 0:
        # convert departure time to seconds
        type = f"substr(departure,1,2) * 3600 + substr(departure, 4,2) * 60 + substr(departure, 7,2)"
        query += get_time_query(departure_time, type)

    if len(arrival_time) > 0:
        # convert arrival time to seconds
        type = f"substr(arrival,1,2) * 3600 + substr(arrival, 4,2) * 60 + substr(arrival, 7,2)"
        query += get_time_query(arrival_time, type)

    columns, rows = db_ops.exec_query(query)

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
    query = f"""SELECT
            code,
            name
            FROM station
        """

    query += f"WHERE UPPER(code) LIKE '{q.upper()}%' or UPPER(name) LIKE '%{q.upper()}%' "

    query += "limit 10"

    columns, rows = db_ops.exec_query(query)

    results = []

    for row in rows:
        results.append(dict(zip(columns,row)))

    return results

def get_schedule(train_number):
    """Returns the schedule of a train.
    """    
    query = f"""SELECT
            station_code,
            station_name,
            day,
            arrival,
            departure
            FROM schedule
            WHERE train_number = {train_number}
        """

    columns, rows = db_ops.exec_query(query)

    results = []

    for row in rows:
        results.append(dict(zip(columns,row)))

    return results

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    train_columns, train_row = db_ops.exec_query(f"select from_station_code, to_station_code from train where number = '{train_number}' limit 1")

    query = f"""
        INSERT INTO booking ('train_number', 'ticket_class', 'date', 'passenger_name', 'passenger_email', 'from_station_code', 'to_station_code')
        VALUES ('{train_number}', '{ticket_class}', '{departure_date}', '{passenger_name}', '{passenger_email}', '{train_row[0][0]}', '{train_row[0][1]}')
    """

    rows = db_ops.exec_insert(query,True)

    return {'train_number' : train_number, 'ticket_class' : ticket_class, 'departure_date' : departure_date,  'passenger_name' : passenger_name, 'passenger_email' : passenger_email }

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    # {
    #     "train_number": "12608",
    #     "train_name": "Lalbagh Exp",
    #     "from_station_code": "SBC",
    #     "from_station_name": "Bangalore",
    #     "to_station_code": "MAS",
    #     "to_station_name": "Chennai",
    #     "ticket_class": "3A",
    #     "date": "2022-09-22",
    #     "passenger_name": "Tourist",
    #     "passenger_email": "tourist@example.com",
    # },

    query = f"""SELECT *
            FROM booking
            WHERE passenger_email = {email}
        """

    columns, rows = db_ops.exec_query(query)

    results = []

    for row in rows:
        results.append(dict(zip(columns,row)))

    return results


    return placeholders.TRIPS
