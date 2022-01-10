import os
PATH_HOME = os.getcwd()
PATH_ROOM = os.path.join(PATH_HOME, "Rooms")
PATH_RES = os.path.join(PATH_HOME,"Reservations")



def main(): 
    import Room, TimeSlot, equipment, utils, Reservation


    print("welcome to the roombooking system")


    keepRun = True

    wrongEntry = True
    while keepRun and wrongEntry:  
        os.chdir(PATH_HOME)
 
        inp01 = input("enter 1 to view all rooms, to exit, enter -1: ")
        if inp01 == "1":
            keepView = True
            while keepView:
                keepView = viewRooms()
                # print("viewRooms")
        elif inp01 == "-1":
            keepRun = False
        else: wrongEntryMsg()
            

def wrongEntryMsg():
    print("Wrong entry, please enter you input again")


def viewRooms():
    import glob, os

    # print(f"in viewRooms(): cwd at {os.getcwd()}")
    os.chdir(PATH_ROOM)
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
        roomNum = input("Enter a number to view details: ") 
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
    
    os.chdir(PATH_HOME)
    
    
def roomDetail(roomFileName):
    import utils, os
    room = utils.fileFile2Room(roomFileName, True)
    print(room)
    wrongEntry = True
    while wrongEntry:
        inp = input("Do you want to book this room? (y/n): ")
        if inp == "y":
            wrongEntry = False
            res,room = bookRoom(room)
            utils.fileRoom2File(room, True)
        elif inp == "n":
            wrongEntry = False
        else: wrongEntryMsg()

    os.chdir(PATH_HOME)
    return 

def bookRoom(room):
    import Reservation
    name = input("please enter your name: ").strip(",")
    contact = input("please enter your contact: ").strip(",")
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

def dateInp():
    wrongInp = True
    while wrongInp:
        wrongInp = False
        dateinp = input("mm-dd-yyyy: ")
        import datetime
        try:
            date = datetime.datetime.strptime(dateinp, "%m-%d-%Y")
        except ValueError:
            print("invalid input! please enter again mm-dd-yyyy")
            wrongInp = True
    return date
def hourInp():
    wrongInp = True
    while wrongInp:
        wrongInp = False
        try: 
            hour = int(input("0<=h<24: "))
            if (hour < 0) or (hour > 23):
                print("invalid input! please enter again 0<=h<24")
                wrongInp = True 
        except ValueError:
            print("invalid input! please enter again 0<=h<24")
            wrongInp = True
    return hour

def quarterInp():
    wrongInp = True
    while wrongInp:
        wrongInp = False
        try: 
            minute = int(input("0<=m<60: "))
            if (minute < 0) or (minute > 60):
                print("invalid input! please enter again 0<=m<60")
                wrongInp = True 
        except ValueError:
            print("invalid input! please enter again 0<=m<60")
            wrongInp = True
    return minute//15
    

def pickTime():
    print("enter your desired start booking date")
    dateHead = dateInp()

    print("enter your desired start booking hour")
    hourHead = hourInp()
        
    print("enter your desired end booking minute")
    quarterHead = quarterInp()
    import TimeSlot
    timehead = TimeSlot.TimePoint(hourHead, quarterHead, dateHead)
    
    print("enter your desired end booking date")
    dateTail = dateInp()

    print("enter your desired end booking hour")
    hourTail = hourInp()
    
    print("enter your desired end booking minute")
    quarterTail = quarterInp()
    timetail = TimeSlot.TimePoint(hourTail, quarterTail, dateTail)
    return TimeSlot.TimeSlot(timehead, timetail)

if __name__ == "__main__":
    main()