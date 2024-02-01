from tkinter import Label, StringVar


# creates a label which displays the page number
def display_page_number(page_window):
    with open("page_number.txt", "r") as f:
        page_number = f.readline()

    v = StringVar()

    label = Label(page_window, textvariable=v, font=("Arial", 15), width=9, height=3, borderwidth=2, relief="ridge")
    label.pack()
    label.place(x=550, y=540)

    v.set("Page: " + page_number)
