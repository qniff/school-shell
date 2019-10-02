#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import sqlite3
import sys
import os
import curses

sys.path.insert(0, './class')
from db import SchoolDatabase
from helper import Helper


# FORMS
# MAIN FORM
class MainForm(npyscreen.ActionForm):
    def create(self):
        courses = self.parentApp.db.list_courses()
        counter = 0
        for course in self.parentApp.db.list_courses():
            text = self.parentApp.helper.print_course(course)
            self.add(OpenCourseButton, name=text)

        self.add(npyscreen.MultiLineEdit, value='\n', max_height=1, editable=False)
        self.add(AddCourseButton, name="*Add course")
        self.add(HelpButton, name="*Help")

    def on_ok(self):
        self.parentApp.change_form(None)

# ADD COURSE FORM
class AddCourseForm(npyscreen.ActionForm):
    def create(self):
        self.courseCode  = self.add(npyscreen.TitleText, name = "Course code: ")
        self.courseName  = self.add(npyscreen.TitleText, name = "Course name: ")

    def on_ok(self):
        self.parentApp.db.add_course(self.courseCode.value, self.courseName.value)
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.change_form("MAIN")

    def on_cancel(self):
        self.parentApp.change_form("MAIN")

# EDIT COURSE FORM
class EditCourseForm(npyscreen.ActionForm):
    def create(self):
        self.course_id = self.parentApp.helper.get_course_id(self.parentApp.currentCourse)
        course = self.parentApp.db.get_course(self.course_id)
        self.courseCode  = self.add(npyscreen.TitleText, name = "Course code: ", value=str(course[1]))
        self.courseName  = self.add(npyscreen.TitleText, name = "Course name: ", value=str(course[2]))

    def on_ok(self):
        self.parentApp.db.update_course(self.course_id, self.courseCode.value, self.courseName.value)
        self.parentApp.currentCourse = self.courseCode.value + ": " + self.courseName.value
        self.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=self.parentApp.currentCourse)
        self.parentApp.change_form("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.change_form("SEE-COURSE")

# SEE COURSE FORM
class SeeCourseForm(npyscreen.ActionForm):
    def create(self):
        # set date of class
        classDate = "Mn: 10:30 - 12:00; Th: 09:00 - 11:00"
        classDate = self.parentApp.db.get_classes()
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        date_record = self.parentApp.db.get_classes(course_id)
        if len(date_record) != 0:
            class_date = date_record[0][2]
            if class_date != '':
                self.add(npyscreen.MultiLineEdit, value="Class schedule: ", max_height=1, editable=False)
                self.add(npyscreen.MultiLineEdit, value="\t\t\t" + class_date, max_height=1, editable=False)
                self.add(npyscreen.MultiLineEdit, value='\n', max_height=1, editable=False)

        # notes buttons
        self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        self.addNotesButton = self.add(AddNotesButton, name="Edit notes")

        # class + course buttons
        self.add(npyscreen.MultiLineEdit, value='\n', max_height=1, editable=False)
        self.editClassButton = self.add(EditClassButton, name="*Edit class schedule")
        self.editCourseButton = self.add(EditCourseButton, name="*Edit course")
        self.deleteCourseButton = self.add(DeleteCourseButton, name="*Delete course")

    def on_ok(self):
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.change_form("MAIN")

    def on_cancel(self):
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.change_form("MAIN")

# SEE NOTES FORM
class SeeNotesForm(npyscreen.ActionForm):
    def create(self):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        content_record = self.parentApp.db.get_notes(course_id)
        if len(content_record) != 0:
            content = content_record[0][2]
            self.notePager = self.add(npyscreen.MultiLineEdit, editable=False, value=content)
    def on_ok(self):
        self.parentApp.change_form("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.change_form("SEE-COURSE")

# ADD NOTES FORM
class AddNotesForm(npyscreen.ActionForm):
    def create(self):
        self.notePager = self.add(npyscreen.MultiLineEdit)
        # set old note
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        old_content_record = self.parentApp.db.get_notes(course_id)
        if len(old_content_record) != 0:
            old_content = old_content_record[0][2]
            self.notePager.value = old_content
            self.notePager.cursor_position = len(old_content)

        self.add_handlers({
            "^X": self.when_cancel,
            "^F": self.when_first,
            "^L": self.when_last,
            "^S": self.when_save
        })

    def when_cancel(self, *args, **keywords):
        self.parentApp.change_form("SEE-COURSE")

    def when_first(self, *args, **keywords):
        self.notePager.cursor_position = 0

    def when_last(self, *args, **keywords):
        self.notePager.cursor_position = len(self.notePager.value)

    def when_save(self, *args, **keywords):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        self.parentApp.db.add_note(course_id, self.notePager.value)
        self.parentApp.change_form("SEE-COURSE")

    def on_ok(self):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        self.parentApp.db.add_note(course_id, self.notePager.value)
        self.parentApp.change_form("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.change_form("SEE-COURSE")

# EDIT CLASS TIME FORM
class EditClassForm(npyscreen.ActionForm):
    def create(self):
        self.classTime  = self.add(npyscreen.TitleText, name = "Class time: ")
        # set old class time
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        old_class_record = self.parentApp.db.get_classes(course_id)

        if len(old_class_record) != 0:
            old_class = old_class_record[0][2]
            self.classTime.value = old_class
            self.classTime.cursor_position = len(old_class)

    def on_ok(self):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        self.parentApp.helper.debug(course_id)
        self.parentApp.helper.debug(self.classTime.value)
        self.parentApp.db.add_class(course_id, self.classTime.value)
        self.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=currentCourse)
        self.parentApp.change_form("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.change_form("SEE-COURSE")

# HELP FORM
class HelpForm(npyscreen.ActionForm):
    def create(self):
        content = "help page"
        with open('README.md', 'r') as file:
            content = file.read()
        self.add(npyscreen.MultiLineEdit, value=content, editable=False)

    def on_ok(self):
        self.parentApp.change_form("MAIN")

    def on_cancel(self):
        self.parentApp.change_form("MAIN")




# MAIN BUTTONS
class AddCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("ADD-COURSE", AddCourseForm, name="Adding course")
        self.parent.parentApp.change_form("ADD-COURSE")

class OpenCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
        self.parent.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=self.name)
        self.parent.parentApp.change_form("SEE-COURSE")

class HelpButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("HELP", HelpForm, name="Help")
        self.parent.parentApp.change_form("HELP")


# COURSE BUTTONS
class DeleteCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        course_id = self.parent.parentApp.helper.get_course_id(self.parent.parentApp.currentCourse)
        self.parent.parentApp.db.delete_course(course_id)
        self.parent.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parent.parentApp.change_form("MAIN")

class EditCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("EDIT-COURSE", EditCourseForm, name="Editing course")
        self.parent.parentApp.change_form("EDIT-COURSE")

class SeeNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("SEE-NOTES", SeeNotesForm, name="Notes")
        self.parent.parentApp.change_form("SEE-NOTES")

class AddNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("ADD-NOTES", AddNotesForm, name="Adding notes")
        self.parent.parentApp.change_form("ADD-NOTES")

class EditClassButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("EDIT-CLASS", EditClassForm, name="Editing class time")
        self.parent.parentApp.change_form("EDIT-CLASS")




# APP
class App(npyscreen.NPSAppManaged):

    currentCourse = 'default'

    def onStart(self):
        self.db = SchoolDatabase()
        self.helper = Helper()
        self.addForm("MAIN", MainForm, name="Welcome to StudentShell")

    def change_form(self,name):
        self.switchForm(name)
        self.resetHistory()


# RUN
if __name__ == "__main__":
    App = App()
    App.run()