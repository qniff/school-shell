#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import sys
import os

# APP
class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Welcome to StudentShell")
        self.addForm("SEE-NOTES", NoteForm, name="Notes")
        self.addForm("ADD-NOTES", NoteForm, name="Notes")

    def change_form(self,name):
        self.switchForm(name)
        self.resetHistory()


# FORMS
class MainForm(npyscreen.ActionForm):
    def create(self):
        self.seeNotesButton = self.add(SeeNotesButton, name="See notes")
        self.seeNotesButton = self.add(AddNotesButton, name="Add notes")
        self.randomButton = self.add(npyscreen.Button, name="Random")

    def on_ok(self):
        self.parentApp.switchForm(None)

class NoteForm(npyscreen.ActionForm):
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


# MAIN BUTTONS
class SeeNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm("SEE-NOTES")

class AddNotesButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm("ADD-NOTES")
# RUN
if __name__ == "__main__":
    App = App()
    App.run()