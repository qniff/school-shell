import sqlite3

class SchoolDatabase(object):
    def __init__(self):
        self.dbfilename = "school.db"
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()

        # course table
        c.execute(
        "CREATE TABLE IF NOT EXISTS course\
            ( course_id INTEGER PRIMARY KEY, \
              code     TEXT, \
              name   TEXT \
              )" \
            )

        # note table
        c.execute(
        "CREATE TABLE IF NOT EXISTS note\
            ( note_id INTEGER PRIMARY KEY, \
              course_id INTEGER, \
              content     TEXT, \
              FOREIGN KEY (course_id) REFERENCES course (course_id) \
              )" \
            )

        # class table
        c.execute(
        "CREATE TABLE IF NOT EXISTS class\
            ( class_id INTEGER PRIMARY KEY, \
              course_id INTEGER, \
              date TEXT, \
              FOREIGN KEY (course_id) REFERENCES course (course_id) \
              )" \
            )
        db.commit()
        c.close()

    def add_course(self, code='', name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO course(code, name) \
                    VALUES(?,?)', (code, name))
        db.commit()
        c.close()

    def get_course(self, course_id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * from course WHERE course_id=?', (course_id,))
        courses = c.fetchall()
        c.close()
        return courses[0]

    def list_courses(self, ):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * from course')
        courses = c.fetchall()
        c.close()
        return courses

    def delete_course(self, course_id=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM course where course_id=?', (course_id,))
        db.commit()
        c.close()

    def update_course(self, course_id, code='', name=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE course set code=?, name=? \
                    course_id=?', (code, name, \
                                                        course_id))

        db.commit()
        c.close()