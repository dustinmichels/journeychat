from datetime import datetime

from journeychat.schemas import room

USERS = [
    {
        "username": "dustin",
        "email": "dustin@dustin.com",
        "password": "dustin",
        "display_name": "Dusty",
    },
    {
        "username": "joe",
        "email": "joe@joe.com",
        "password": "joe",
        "display_name": "Joe",
    },
]


ROOMS = [
    {
        "name": "General",
        "is_private": False,
    },
    {
        "name": "Sci-Fi Lovers",
        "is_private": False,
    },
    {
        "name": "Python Fans",
        "is_private": False,
    },
    {"name": "Dustin's Room", "is_private": True, "owner_id": 2},
]


MESSAGES = [
    {
        # "email": "dustin@dustin.com",
        "user_id": 2,
        "room_id": 1,
        "timestamp": datetime(2021, 10, 4, 2, 20, 35),
        "text": "hello friends!",
    }
]
