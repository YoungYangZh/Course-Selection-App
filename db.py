import sqlite3
import os
from sqlalchemy import create_engine

engine=create_engine('sqlite:///courses.db')

class DB:

    def __init__(self, db_url: str):
        self.db_url = db_url

        if not os.path.exists(self.db_url):
            self.courses_db()
            self.info_db()
            self.course_db()

    def call_db(self, query, *args):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def courses_db(self):
        courses_db_query = """
        CREATE TABLE IF NOT EXISTS courses (
            courses_id INTEGER PRIMARY KEY,
            courses_name TEXT NOT NULL,
            teacher TEXT NOT NULL
        );
        """
        self.call_db(courses_db_query)

    def course_db(self):
        course_db_query = """
        CREATE TABLE IF NOT EXISTS course (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            teacher TEXT NOT NULL
        );
        """
        self.call_db(course_db_query)

    def info_db(self):
        info_db_query = """
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact INTEGER NOT NULL
        );
        """
        self.call_db(info_db_query)
      