import json
from db import DB

db = DB("courses.db")

create_courses = """
INSERT INTO courses (
courses_name, 
teacher
) VALUES (
?, ?
)
"""

with open("seed.json", "r") as seed:
    data = json.load(seed)

    for courses in data:
        db.call_db(create_courses, courses["courses_name"], courses["teacher"])