import os
import sqlite3
import tkinter

from tkinter.ttk import Label
from tkinter import messagebox, END

from tinydb import TinyDB, where
from tinydb import Query

import picturesDisplay


def create_new_window(delete_window):
    new_window = tkinter.Toplevel()
    new_window.geometry("350x150")

    # validation for first image number in range
    def validate_text_first():
        value_first = int(first.get())
        if value_first < 1:
            tkinter.messagebox.showerror('Image number must be at minimum 1.                              ')
            first.delete(0, END)
            first.insert(0, "1")
            return False
        elif value_first > 24:
            tkinter.messagebox.showerror('Image number must be at maximum 24.                              ')
            first.delete(0, END)
            first.insert(0, "24")
            return False
        else:
            return True

    # validation for last image number in range
    def validate_text_last():
        value_last = int(last.get())
        if value_last < 1:
            tkinter.messagebox.showerror('Image number must be at minimum 1.                              ')
            last.delete(0, END)
            last.insert(0, "1")
            return False
        elif value_last > 24:
            tkinter.messagebox.showerror('Image number must be at maximum 24.                              ')
            last.delete(0, END)
            last.insert(0, "24")
            return False
        else:
            return True

    # validation for difference in image number in range
    def validate_text_difference():
        value_first = int(first.get())
        value_last = int(last.get())
        if value_last < value_first:
            tkinter.messagebox.showerror('The last image number must be more than the first image number.                              ')
            last.delete(0, END)
            last.insert(0, str(value_first))
            return False
        else:
            return True

    label1 = Label(new_window, text="Pictures from: ")
    label1.pack()
    label1.place(x=20, y=40)

    first = tkinter.Entry(new_window, width=2)
    first.pack()
    first.place(x=105, y=40)

    label2 = Label(new_window, text="to")
    label2.pack()
    label2.place(x=125, y=40)

    last = tkinter.Entry(new_window, width=2)
    last.pack()
    last.place(x=145, y=40)

    # command for the delete button
    def delete_command():
        first_boolean = validate_text_first()
        last_boolean = validate_text_last()
        difference_boolean = validate_text_difference()

        if first_boolean is True and last_boolean is True and difference_boolean is True:
            database = sqlite3.connect("image.db")
            cursor = database.cursor()
            db = TinyDB(os.path.abspath("./db.json"))
            first_picture = int(first.get())
            last_picture = int(last.get())
            count = 1

            rowid = Query()

            while first_picture <= last_picture:
                actual_id = db.get(rowid.picture_id == first_picture-1)
                print("1")
                cursor.execute("""
                DELETE FROM image_table WHERE rowid = ?
                """, (actual_id.get("row_id"),))
                db.remove(where("picture_id") == str(first_picture))
                print("2")
                first_picture += 1
                count += 1

            database.commit()
            cursor.close()
            database.close()

            # update displayed pictures
            picturesDisplay.display_pictures(delete_window)

    # button to delete pictures
    rename_picture = tkinter.Button(
        new_window, text="Delete Pictures", command=delete_command, height=3, width=20
    )
    rename_picture.place(x=100, y=95)
