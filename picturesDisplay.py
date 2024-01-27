import os
import sqlite3
from tinydb import TinyDB
from tkinter import Label

import PIL
from PIL import Image, ImageTk

import pageDisplay


def display_pictures(picture_window):
    # display page number
    pageDisplay.display_page_number(picture_window)

    database = sqlite3.connect("image.db")
    cursor = database.cursor()
    write_data = 0

    db = TinyDB(os.path.abspath("./db.json"))
    db.truncate()

    # count number of records from table
    cursor.execute("""SELECT COUNT(*) FROM image_table""")
    records_number = cursor.fetchone()[0]

    with open("page_number.txt", "r") as f:
        page_number = int(f.readline())

    # change record number depending on pages
    records_number = records_number-(24*page_number)+24

    for i in range(24):
        # offset image to next image
        offset = i+(24*page_number)-24

        if i < records_number:
            # read byte data from table
            m = cursor.execute("""
            SELECT * FROM image_table LIMIT 1 OFFSET
            """ + str(offset))

            for x in m:
                write_data = x[2]
                db.insert({'picture_id': i, 'row_id': x[0]})

            # write byte data to image file
            with open(os.path.abspath("./pictures/picture_" + str(i) + ".png"), "wb") as f:
                f.write(write_data)

        else:
            # replace unused labels with blank pictures
            with open(os.path.abspath("./pictures/blank.png"), "rb") as f:
                data = f.read()
            with open(os.path.abspath("./pictures/picture_" + str(i) + ".png"), "wb") as f:
                f.write(data)

    cursor.close()

    x = -1
    y = 0
    images = []
    for i in range(24):
        x += 1
        if x % 6 == 0:
            y += 100
            x = 0
        # resize then append picture file from database to array
        images.append(ImageTk.PhotoImage(Image.open(os.path.abspath(
            "./pictures/picture_" + str(i) + ".png")).resize((100, 100), PIL.Image.Resampling.LANCZOS)))

        # display label with image
        label = Label(picture_window, image=images[-1], width=100, height=100, borderwidth=2, relief="ridge")
        label.pack()
        label.place(x=50+(x*100), y=40+y)

        label1 = Label(picture_window, text=i+1)
        label1.pack()
        label1.place(x=51+(x*100), y=41+y)

    picture_window.mainloop()
