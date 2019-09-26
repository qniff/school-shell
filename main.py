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
            self.add(OpenCourse, name=text)
            counter += 1

    def on_ok(self):
        self.parentApp.switchForm(None)

class SeeCourseForm(npyscreen.ActionForm):
    def create(self):
        text = self.parentApp.currentCourse
        course_id = self.parentApp.helper.get_course_id(text)
        self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        self.addNotesButton = self.add(AddNotesButton, name="Add notes")

    def on_ok(self):
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

class SeeNotesForm(npyscreen.ActionForm):
    def create(self):
        self.notePager = self.add(npyscreen.Pager, name="note", editable=False)

        self.notePager.values = "sample"
    def on_ok(self):
        self.parentApp.switchForm("SEE-COURSE")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

class AddNotesForm(npyscreen.ActionForm):
    def create(self):
        self.notePager = self.add(npyscreen.MultiLineEdit)
        self.add_handlers({
            "^A": self.when_save_note,
            "^X": self.when_back,
        })
        f = open("whatever", "a")
        f.write(self.notePager.value)
        f.close()

    def when_save_note(self, *args, **keywords):
        f = open("whatever", "a")
        f.write(self.notePager.value)
        f.close()

    def when_back(self, *args, **keywords):
        self.parentApp.switchForm("MAIN")


# MAIN BUTTONS
class OpenCourse(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
        self.parent.parentApp.addForm("SEE-COURSE", SeeCourseForm, name=self.name)
        self.parent.parentApp.change_form("SEE-COURSE")

class SeeNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
        self.parent.parentApp.addForm("SEE-NOTES", SeeNotesForm, name="Notes")
        self.parent.parentApp.switchForm("SEE-NOTES")

class AddNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.currentCourse = self.name
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
