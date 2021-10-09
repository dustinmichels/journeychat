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
    {
        "username": "sam",
        "email": "sam@sam.com",
        "password": "sam",
        "display_name": "Sam",
    },
    {
        "username": "mike123",
        "email": "mike@sam.com",
        "password": "mike",
        "display_name": "Mikey",
    },
]


ROOMS = [
    {
        "name": "General",
        "is_private": False,
    },
    {
        "name": "Sci-Fi Readers",
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
        "user_id": 2,
        "room_id": 1,
        "timestamp": datetime(2021, 10, 4, 2, 20, 35),
        "text": "Hello friends!",
    },
    {
        "user_id": 3,
        "room_id": 1,
        "timestamp": datetime(2021, 10, 4, 2, 25, 35),
        "text": "What's up?",
    },
    {
        "user_id": 4,
        "room_id": 1,
        "timestamp": datetime(2021, 10, 4, 2, 27, 35),
        "text": "Coding is fun.",
    },
    {
        "user_id": 2,
        "room_id": 2,
        "timestamp": datetime(2021, 10, 4, 2, 20, 35),
        "text": "Kim Stanley Robinson is a cool author to check out!",
    },
    {
        "user_id": 2,
        "room_id": 3,
        "timestamp": datetime(2021, 10, 4, 3, 20, 35),
        "text": "Python is cool",
    },
    {
        "user_id": 3,
        "room_id": 3,
        "timestamp": datetime(2021, 10, 4, 3, 22, 35),
        "text": "Agreed.",
    },
]
