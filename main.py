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
        # self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        # self.seeNotesButton = self.add(AddNotesButton, name="Add notes")
        courses = self.parentApp.db.list_courses()
        text = str(len(courses))
        text = courses[1]

        text0 = self.parentApp.helper.print_course(courses[1])


        text = self.parentApp.helper.print_course(courses[0])


        t  = self.add(npyscreen.TitleText, name = 'Text: ', value=text0)
        t1  = self.add(npyscreen.TitleText, name = 'Text: ', value=text)

        # self.two = self.add(npyscreen.Button, name=(text0))



    def on_ok(self):
        self.parentApp.switchForm(None)

# SEE NOTES FORM
class SeeNotesForm(npyscreen.ActionForm):
    def create(self):
        self.notePager = self.add(npyscreen.Pager, name="note", editable=False)

        with open("nut") as f:
            note = f.readlines()

        # note = os.popen("cat nut").read()
        self.notePager.values = [note]
    def on_ok(self):
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

# ADD NOTES FORM
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
class SeeNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm("SEE-NOTES")

class AddNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm("ADD-NOTES")


# APP
class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.db = SchoolDatabase()
        self.helper = Helper()
        self.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.addForm("SEE-NOTES", SeeNotesForm, name="Notes")
        self.addForm("ADD-NOTES", AddNotesForm, name="Notes")

    def change_form(self,name):
        self.switchForm(name)
        self.resetHistory()

# RUN
if __name__ == "__main__":
    App = App()
    App.run()
