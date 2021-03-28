from tkinter import *
from JanggiGame import *

class Janggi_GUI:

	def __init__(self, master):
		self.master = master
		master.title("Janggi")
		master.geometry("500x500")



root = Tk()
play_Janggi = Janggi_GUI(root)
root.mainloop()
