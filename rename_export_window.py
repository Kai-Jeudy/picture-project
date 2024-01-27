import io
import os
import sqlite3
import tkinter
import tkinter as tk

from tkinter.ttk import Label
from tkinter import messagebox, END, filedialog, DISABLED

from tinydb import TinyDB
from tinydb import Query

from PIL import Image

import shutil


def create_new_window():
    new_window = tkinter.Toplevel()
    new_window.geometry("650x150")

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

    label3 = Label(new_window, text="Rename to: ")
    label3.pack()
    label3.place(x=200, y=40)

    rename = tkinter.Text(new_window, height=1, width=15)
    rename.pack()
    rename.place(x=270, y=40)

    # button command for renaming pictures
    def rename_command():
        first_boolean = validate_text_first()
        last_boolean = validate_text_last()
        difference_boolean = validate_text_difference()

        if first_boolean is True and last_boolean is True and difference_boolean is True:
            database = sqlite3.connect("image.db")
            cursor = database.cursor()
            db = TinyDB(os.path.abspath("./db.json"))
            new_name = rename.get("1.0", "end-1c")
            first_picture = int(first.get())
            last_picture = int(last.get())
            count = 1

            rowid = Query()

            while first_picture <= last_picture:
                actual_id = db.get(rowid.picture_id == first_picture-1)

                cursor.execute("""
                UPDATE image_table SET name = ? WHERE rowid = ?
                """, (new_name + "_" + str(count), actual_id.get("row_id")))
                first_picture += 1
                count += 1

            # enable export button once rename button is used
            export_picture.config(state=tk.NORMAL)

            database.commit()
            cursor.close()
            database.close()

    # button command for exporting pictures
    def export_command():
        first_boolean = validate_text_first()
        last_boolean = validate_text_last()
        difference_boolean = validate_text_difference()
        folder_path = filedialog.askdirectory()

        if first_boolean is True and last_boolean is True and difference_boolean is True:
            database = sqlite3.connect("image.db")
            cursor = database.cursor()
            first_picture = int(first.get())
            last_picture = int(last.get())
            name_data = 0
            image_data = 0

            while first_picture <= last_picture:
                offset = first_picture-1
                print(offset)
                m = cursor.execute("""
                SELECT * FROM image_table LIMIT 1 OFFSET
                """ + str(offset))

                for x in m:
                    name_data = x[1]
                    image_data = x[2]

                imported_image = Image.open(io.BytesIO(image_data))
                imported_image.save(str(name_data) + ".png", "PNG")

                shutil.move(str(name_data) + ".png", folder_path)

                first_picture += 1

            # disable export button after being used once
            export_picture.config(state=tk.DISABLED)

            database.commit()
            cursor.close()
            database.close()

    # button to rename pictures
    rename_picture = tkinter.Button(
        new_window, text="Rename Pictures", command=rename_command, height=3, width=20
    )
    rename_picture.place(x=100, y=95)

    # button to export pictures
    export_picture = tkinter.Button(
        new_window, text="Export Pictures", command=export_command, height=3, width=20, state=DISABLED
    )
    export_picture.place(x=385, y=95)
