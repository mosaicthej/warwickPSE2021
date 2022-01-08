from tkinter.constants import W


def main(): 
    import Room, TimeSlot, equipment, utils, Reservation


    print("welcome to the roombooking system")


    keepRun = True


    while keepRun:
        wrongEntry = True
        while wrongEntry and keepRun:
            inp01 = input("enter 1 to view all rooms, to exit, enter -1")
            if inp01 == "1":
                keepView = False
                while keepView:
                    keepView = viewRooms()
            elif inp01 == "-1":
                keepRun = False
            else: wrongEntryMsg()
                

def wrongEntryMsg():
    print("Wrong entry, please enter you input again")


def viewRooms():
    import glob, os
    
    os.chdir("Rooms")
    roomFiles = []
    roomNames = []
    i = 0
    for file in glob.glob("*.txt"):
        roomNames.append(str(i)+"-"+file)
        i += 1
        roomFiles.append(file)
    
    print("we have following rooms:")
    for room in roomNames:
        print(room, end="\t")
    
    wrongEntry = True; keepView = False;
    while wrongEntry:
        roomNum = input("Enter a number to view details") 
        if roomNum.isnumeric():
            roomNum = int(roomNum)
            if 0<=roomNum and roomNum <= len(roomNames):
                wrongEntry = False
                roomF = roomFiles[roomNum]
                roomDetail(roomF)
            else:
                wrongEntryMsg()
        else:
            wrongEntryMsg()
    
    os.chdir("/..")
    
    
def roomDetail(roomFileName):
    import utils, os
    room = utils.fileFile2Room(roomFileName, True)
    print(room)
    wrongEntry = True
    while wrongEntry:
        inp = input("Do you want to book this room? (y/n)")
        if inp == "y":
            wrongEntry = False
            res,room = bookRoom(room)
            utils.fileRoom2File(room, True)
            
            os.chdir("/..")
            utils.fileReservation2File(res)
            os.chdir("Rooms")
        elif inp == "n":
            wrongEntry = False
        else: wrongEntryMsg()
    return 

def bookRoom(room):
    import Reservation
    name = input("please enter your name").strip(",")
    contact = input("please enter your contact").strip(",")
    roomName = room.get_id()
    print("booking for "+roomName+"...")
    print("room is available at following timeslots:")
    avaList = room.get_availability()
    for ava in avaList:
        print(ava)
    conflict = True
    while conflict:
        timeSlot = pickTime()
        if room.availiableAt(timeSlot):
            conflict = False
        else: 
            print("there is a time conflict, please choose another time")
    room.bookAt(timeSlot)
    res = Reservation.Reservation(name, contact, roomName, timeSlot)
    return (res, room)

def pickTime():
    print("enter your desired start booking date")
    dateinpHead = input("mm/dd/yyyy")
    dateinpListHead = dateinpHead.split("/")
    dateStrHead = "%"+dateinpListHead[0]+"-%"+dateinpListHead[1]+"-%"+dateinpListHead[2]
    import datetime
    dateHead = datetime.datetime.strptime(dateStrHead, "%Y-%m-%d")
    print("enter your desired start booking hour")
    hourHead = int(input("0<=h<24: "))
    print("enter your desired end booking minute")
    quarterHead = int(input("0<=m<60"))//15
    import TimeSlot
    timehead = TimeSlot.TimePoint(hourHead, quarterHead, dateHead)
    
    print("enter your desired end booking date")
    dateinpTail = input("mm/dd/yyyy")
    dateinpListTail = dateinpTail.split("/")
    dateStrTail = "%"+dateinpListTail[0]+"-%"+dateinpListTail[1]+"-%"+dateinpListTail[2]
    dateTail = datetime.datetime.strptime(dateStrTail, "%Y-%m-%d")
    print("enter your desired end booking hour")
    hourTail = int(input("0<=h<24: "))
    print("enter your desired end booking minute")
    quarterTail = int(input("0<=m<60"))//15
    timetail = TimeSlot.TimePoint(hourTail, quarterTail, dateTail)
    return TimeSlot.TimeSlot(timehead, timetail)

if __name__ == "__main__":
    main()