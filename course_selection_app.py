from typing import List
import requests
from api import Course
from api import Info
import pandas as pd
from sqlalchemy import create_engine
from db import engine 


def url(route: str):
    return f"http://127.0.0.1:8000{route}"


print("Hello from Course Selection app")


def print_menu():
    print(
        """
    1: Show Courses
    2: Choose Course
    3: Show the course you have chosen
    4: Delete Course
    5: Update Course
    6: Put in your info
    7: Exit program
    """
    )
    pass

def show_courses():
    res=requests.get(url('/courses'))
    print(res.json())

def choose_course():
    print("Choose course")
    course_name = input("Course name: ")
    teacher = input("Teacher: ")
    new_course = Course(course_name=course_name, teacher=teacher)
    res = requests.post(url("/add_course"), json=new_course.dict())
    print(res.json())


def get_course():
    choose_course = []
    print("Get course")
    res = requests.get(url("/get_course"))
    if not res.status_code == 200:
        return
    data = res.json()
    for course in data: 
        course = Course(**course) 
        print("_________")
        print(f"ID: {course.id}")
        print(f"Course_name: {course.course_name}")
        print(f"Teacher: {course.teacher}")
        choose_course.append(course)
    print(choose_course)
    return choose_course

def add_info():
    print("Put your information")
    name = input("Name: ")
    contact = input("Contact: ")
    new_info = Info(name=name, contact=contact)
    res = requests.post(url("/add_info"), json=new_info.dict())
    print(res.json())


def delete_course():
    print("Delete course")
    course_to_delete = input("Id of course you wish to delete: ")
    if not str.isdigit(course_to_delete):
        print("Ids are integers")
        return
    res = requests.delete(url(f"/delete_course/{course_to_delete}"))
    print(res)


def update_course(choose_course: List[Course]):
    print("Update course", choose_course)
    course_to_update = input("Id of course you wish to update: ")
    if not str.isdigit(course_to_update):
        print("Ids are integers")
        return

    index = None
    for i, course in enumerate(choose_course):
        print(course.id)
        if course.id == int(course_to_update):
            index = i
            break

    if index == None:
        print("No such course")
        return
    course = choose_course[index]

    course_name = input("Course name (leave blank if same): ")
    teacher = input("Course teacher (Leave blank if same): ")

    if not course_name:
        course_name = course.course_name
    if not teacher:
        teacher = course.teacher

    new_course = Course(course_name=course_name, teacher=teacher)
    res = requests.put(url(f"/update_course/{course_to_update}"), json=new_course.dict())
    print(res)


def main():
    print_menu()
    choice = input("Please choose your action: ")
    choice = choice.strip()
    if not str.isdigit(choice):
        print("Please enter a valid option")
        return

    match int(choice):
        case 1:
            show_courses()
        case 2:
            choose_course()
        case 3:
            get_course()
        case 4:
            delete_course()
        case 5:
            course_get=get_course()
            update_course(course_get)
        case 6:
            add_info()
        case 7:
            exit()
        case _:
            print("Please enter a valid choice")


while __name__ == "__main__":
    main()