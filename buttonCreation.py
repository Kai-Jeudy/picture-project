import math
import os
import sqlite3
import tkinter
from tkinter import filedialog

import delete_window
import rename_export_window

import picturesDisplay


def buttons_create(button_window):
    # button functions

    # add_picture command for the "+" button
    def add_picture_command():
        database = sqlite3.connect("image.db")
        cursor = database.cursor()

        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)
        name = os.path.splitext(file_name)[0]

        # read binary from file
        with open(file_path, "rb") as f:
            data = f.read()

        # insert data to table
        cursor.execute("""
        INSERT INTO image_table (name, data) VALUES (?, ?)
        """, (name, data))

        database.commit()
        cursor.close()
        database.close()

        # update displayed pictures
        picturesDisplay.display_pictures(button_window)

    # delete_picture command for "-" button
    def delete_picture_command():
        delete_window.create_new_window(button_window)

    # organise_picture command for "🗘" button
    def organise_pictures_command():
        rename_export_window.create_new_window()

    # display previous page
    def left_page_command():
        with open("page_number.txt", "r") as f:
            page_number = int(f.readline())

        if page_number > 1:
            page_number -= 1

        print(str(page_number))

        with open("page_number.txt", "w") as f:
            f.write(str(page_number))

        # update displayed pictures
        picturesDisplay.display_pictures(button_window)

    # display next page
    def right_page_command():
        database = sqlite3.connect("image.db")
        cursor = database.cursor()

        # count number of records from table
        cursor.execute("""SELECT COUNT(*) FROM image_table""")
        records_number = cursor.fetchone()[0]
        print(records_number)
        print(int(math.ceil(records_number/24)))

        with open("page_number.txt", "r") as f:
            page_number = int(f.readline())

        if int(math.ceil(records_number/24)) > page_number:
            page_number += 1

        with open("page_number.txt", "w") as f:
            f.write(str(page_number))

        # update displayed pictures
        picturesDisplay.display_pictures(button_window)

        cursor.close()

    # button to add picture
    button_window.add_picture_image = tkinter.PhotoImage(file="add_image.png")
    add_picture = tkinter.Button(
        button_window, image=button_window.add_picture_image, command=add_picture_command, height=60, width=60
    )
    add_picture.place(x=0, y=0)

    # button to delete picture
    button_window.delete_picture_image = tkinter.PhotoImage(file="delete_image.png")
    delete_picture = tkinter.Button(
        button_window, image=button_window.delete_picture_image, command=delete_picture_command, height=60, width=60
    )
    delete_picture.place(x=60, y=0)

    # button to organise pictures
    button_window.organise_picture_image = tkinter.PhotoImage(file="organise_image.png")
    organise_picture = tkinter.Button(
        button_window, image=button_window.organise_picture_image, command=organise_pictures_command, height=60, width=60
    )
    organise_picture.place(x=120, y=0)

    # button to display previous page
    button_window.left_page_image = tkinter.PhotoImage(file="page_left.png")
    left_page = tkinter.Button(
        button_window, image=button_window.left_page_image, command=left_page_command, height=60, width=247.5
    )
    left_page.place(x=50, y=540)

    # button to display next page
    button_window.right_page_image = tkinter.PhotoImage(file="page_right.png")
    right_page = tkinter.Button(
        button_window, image=button_window.right_page_image, command=right_page_command, height=60, width=247.5
    )
    right_page.place(x=297.5, y=540)
