from tkinter import *
from PIL import ImageTk, Image
from JanggiGame import *


root = Tk()
root.title("Janggi")

status_frame = LabelFrame(root)

status_frame.grid(row=0, column=0)

status_label = Label(status_frame, text="Game Status:")
status_label.grid(row=0, column=0)

board_frame = LabelFrame(root)
board_frame.grid(row=1, column=0)

background_image = ImageTk.PhotoImage(Image.open("images/janggi_board.png"))
background_label = Label(image=background_image)
background_label.grid(row=1, column=0)

root.mainloop()
