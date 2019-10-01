#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import sqlite3
import sys
import os

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

    def on_ok(self):
        self.parentApp.switchForm(None)

# ADD COURSE FORM
class AddCourseForm(npyscreen.ActionForm):
    def create(self):
        self.courseCode  = self.add(npyscreen.TitleText, name = "Course code: ")
        self.courseName  = self.add(npyscreen.TitleText, name = "Course name: ")

    def on_ok(self):
        self.parentApp.db.add_course(self.courseCode.value, self.courseName.value)
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

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
        self.parentApp.switchForm("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.switchForm("SEE-COURSE")

# SEE COURSE FORM
class SeeCourseForm(npyscreen.ActionForm):
    def create(self):
        self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        self.addNotesButton = self.add(AddNotesButton, name="Edit notes")
        self.add(npyscreen.MultiLineEdit, value='\n', max_height=1, editable=False)
        self.editCourseButton = self.add(EditCourseButton, name="*Edit course")
        self.deleteCourseButton = self.add(DeleteCourseButton, name="*Delete course")

    def on_ok(self):
        self.parent.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.switchForm("MAIN")

# SEE NOTES FORM
class SeeNotesForm(npyscreen.ActionForm):
    def create(self):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        self.notePager = self.add(npyscreen.Pager, name="note", editable=False)
        content_record = self.parentApp.db.get_notes(course_id)
        self.parentApp.helper.debug(str(len(content_record)))
        if len(content_record) != 0:
            content = content_record[0][2]
            self.notePager.values = content
    def on_ok(self):
        self.parentApp.switchForm("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.switchForm("SEE-COURSE")

# ADD NOTES FORM
class AddNotesForm(npyscreen.ActionForm):
    def create(self):
        self.notePager = self.add(npyscreen.MultiLineEdit)
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        old_content_record = self.parentApp.db.get_notes(course_id)

        self.parentApp.helper.debug(str(len(old_content_record)))
        if len(old_content_record) != 0:
            old_content = old_content_record[0][2]
            self.notePager.value = old_content

    def on_ok(self):
        currentCourse = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(currentCourse)
        self.parentApp.db.add_note(course_id, self.notePager.value)
        self.parentApp.switchForm("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.switchForm("SEE-COURSE")


# MAIN BUTTONS
class AddCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("ADD-COURSE", AddCourseForm, name="Adding course")
        self.parent.parentApp.switchForm("ADD-COURSE")

class OpenCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
        self.parent.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=self.name)
        self.parent.parentApp.switchForm("SEE-COURSE")


# COURSE BUTTONS
class DeleteCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        course_id = self.parent.parentApp.helper.get_course_id(self.parent.parentApp.currentCourse)
        self.parent.parentApp.db.delete_course(course_id)
        self.parent.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parent.parentApp.switchForm("MAIN")

class EditCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("EDIT-COURSE", EditCourseForm, name="Editing course")
        self.parent.parentApp.switchForm("EDIT-COURSE")

class SeeNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("SEE-NOTES", SeeNotesForm, name="Notes")
        self.parent.parentApp.switchForm("SEE-NOTES")

class AddNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.addForm("ADD-NOTES", AddNotesForm, name="Adding notes")
        self.parent.parentApp.switchForm("ADD-NOTES")


# APP
class App(npyscreen.NPSAppManaged):

    currentCourse = 'default'

    def onStart(self):
        self.db = SchoolDatabase()
        self.helper = Helper()
        self.addForm("MAIN", MainForm, name="Welcome to StudentShell")


# RUN
if __name__ == "__main__":
    App = App()
    App.run()