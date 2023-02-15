from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from db import DB
from db import engine

class Course(BaseModel):
    id: int = None
    course_name: str
    teacher: str

class Info(BaseModel):
    id: int = None
    name: str
    contact: int

class Courses(BaseModel):
    id:int=None
    course_name:str
    teacher:str

app = FastAPI()
db = DB("courses.db")

app.curr_id = 1
app.course_choose: List[Course] = []
app.info: List[Info] = []


@app.get("/")
def root():
    return "Hello and welcome to select courses!"

@app.get('/courses')
def show_courses():
    df=pd.read_sql_query('SELECT * FROM courses',engine)
    print(df)
    return df.to_json()


@app.get("/get_course")
def get_course_choose():
    get_course_query = """
    SELECT * FROM course
    """
    data = db.call_db(get_course_query)
    choose_course = []
    for element in data:
        id, course_name, teacher = element
        choose_course.append(Course(id=id, course_name=course_name, teacher=teacher))
    print(data)
    return choose_course
    

@app.post("/add_course")
def add_course(course: Course):
    insert_query = """
    INSERT INTO course (course_name, teacher)
    VALUES ( ?, ? )
    """
    db.call_db(insert_query, course.course_name, course.teacher)
    return "Adds a task"

@app.post("/add_info")
def add_info(info: Info):
    insert_query = """
    INSERT INTO info (name, contact)
    VALUES ( ?, ? )
    """
    db.call_db(insert_query, info.name, info.contact)
    return "Adds an info"

@app.delete("/delete_course/{course_id}")
def delete_course(course_id: int):
    delete_query = """
    DELETE FROM course WHERE course_id = ?
    """
    db.call_db(delete_query, course_id)
    return True


@app.put("/update_course/{id}")
def update_course(id: int, new_course: Course):
    update_course_query = """
    UPDATE course
    SET course_name = ?, teacher = ?
    WHERE course_id = ?
    """

    db.call_db(update_course_query, new_course.course_name, new_course.teacher, id)
    return True