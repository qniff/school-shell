#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import sqlite3
import sys
import os

from db import SchoolDatabase
from help import Helper

# FORMS
class MainForm(npyscreen.ActionForm):
    def create(self):
        courses = self.parentApp.db.list_courses()
        counter = 0
        for course in self.parentApp.db.list_courses():
            text = self.parentApp.helper.print_course(courses[counter])
            self.add(OpenCourseButton, name=text)
            counter += 1

        # self.add(npyscreen.TitleText, value='=====')
        self.add(AddCourseButton, name="*Add course")

    def on_ok(self):
        self.parentApp.switchForm(None)

class AddCourseForm(npyscreen.ActionForm):
    def create(self):
        self.courseCode  = self.add(npyscreen.TitleText, name = "Course code: ")
        self.courseName  = self.add(npyscreen.TitleText, name = "Course name: ")

    def on_ok(self):
        # Save course
        self.parentApp.db.add_course(self.courseCode.value, self.courseName.value)
        self.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

class SeeCourseForm(npyscreen.ActionForm):
    def create(self):
        self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        self.addNotesButton = self.add(AddNotesButton, name="Edit notes")
        self.deleteCourseButton = self.add(DeleteCourseButton, name="*Delete course")

    def on_ok(self):
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

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

class DeleteCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        course_id = self.parent.parentApp.helper.get_course_id(self.parent.parentApp.currentCourse)
        self.parent.parentApp.db.delete_course(course_id)
        self.parent.parentApp.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.parent.parentApp.switchForm("MAIN")

class OpenCourseButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
        self.parent.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=self.name)
        self.parent.parentApp.change_form("SEE-COURSE")

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
        # self.addForm("SEE-COURSE", SeeCourseForm, name="COURSE INFO")
        # self.addForm("SEE-NOTES", SeeNotesForm, name="Notes")
        # self.addForm("ADD-NOTES", AddNotesForm, name="Notes")

    def change_form(self,name):
        self.switchForm(name)
        self.resetHistory()

# RUN
if __name__ == "__main__":
    App = App()
    App.run()


# USEFUL STUFF
        # self.add_handlers({
        #     "^A": self.when_save_note,
        #     "^X": self.when_back,
        # })
        # f.write(self.notePager.value)
        # f.close()

    # def when_save_note(self, *args, **keywords):
    #     f = open("whatever", "a")
    #     f.write(self.notePager.value)
    #     f.close()