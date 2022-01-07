from tkinter import *
from tkinter import ttk
import Room, TimeSlot, utils

with open("equipment.txt","r") as eqF:
    allEquipmentSet = set(
        eqF.read().split("\n")
    )
root = Tk()
root.title("welcome to booking system")
margin_x = 5; margin_y = 8

rootWidth, rootHeight = 800, 700

root.geometry("%dx%d"%(rootWidth,rootHeight))

# getting list of rooms
fullRoomList = utils.allRoomNameInDir()

textLableRooms = Label(root, textvariable="Rooms:")


RoomsCombo = ttk.Combobox(root, value=fullRoomList).place(x = 60, y = 8)



textLableRooms.pack()
root.mainloop()
