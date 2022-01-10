from tkinter import *
from tkinter import ttk

root_window = Tk()

lab_welcom = Label(root_window, text= "Welcome to the Room Booking System!")
lab_welcom.grid(row=0, column=0)

frm_roomList = Frame(root_window)
lab_allRooms = Label(frm_roomList, text="All Rooms \n(or filtered results)")
lab_allRooms


frm_roomList.grid(row=1, column=0)

root_window.mainloop()