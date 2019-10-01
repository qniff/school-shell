import sqlite3
from datetime import datetime

class Helper:
    def print_course(self, course=''):
        return course[1] + ': ' + course[2]

    def get_course_id(self, text=''):
        code = text.split(':')[0]
        db = sqlite3.connect('school.db')
        c = db.cursor()
        c.execute('SELECT course_id from course WHERE code=?', (code,))
        course_id = str(c.fetchone()[0])
        c.close()
        return course_id

    def debug(self, message=''):
        f = open("debug.txt", "a")
        f.write(str(datetime.now()) + ": " + str(message) + "\n")
        f.close()