import tkinter

import pageDisplay

import databaseCreation
import picturesDisplay
import buttonCreation

# creates the initial GUI window
window = tkinter.Tk()
window.geometry("800x600")

# each step is done in order
databaseCreation.create_database()

pageDisplay.display_page_number(window)

buttonCreation.buttons_create(window)

picturesDisplay.display_pictures(window)

window.mainloop()
