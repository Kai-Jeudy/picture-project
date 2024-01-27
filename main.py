import tkinter

import pageDisplay

import databaseCreation
import picturesDisplay
import buttonCreation

window = tkinter.Tk()
window.geometry("800x600")

databaseCreation.create_database()

pageDisplay.display_page_number(window)

buttonCreation.buttons_create(window)

picturesDisplay.display_pictures(window)

window.mainloop()
