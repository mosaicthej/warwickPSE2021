# Python3 Program for recursive binary search.
# Returns index of x in arr if present, else -1
def binarySearch(arr, l, r, x):

	# Check base case
	if r >= l:
		mid = l + (r - l) // 2
		# If element is present at the middle itself
		if arr[mid] == x:
			return mid

		# If element is smaller than mid, then it
		# can only be present in left subarray
		elif arr[mid] > x:
			return binarySearch(arr, l, mid-1, x)

		# Else the element can only be present
		# in right subarray
		else:
			return binarySearch(arr, mid + 1, r, x)

	else:
		# Element is not present in the array
		return -1


# utils for file reading and writing.
# saving all data using a .csv file
import datetime
# for details, see roomTemplate.csv and reservationTemplate.csv
def fileStr2EquipmentSet(fileStr: str) -> set[str]:
    """file util function: convert a line in saved data file to set of equipment
    Args:
        fileStr (str): a string in data file
    Returns:
        set[str]: a set containing all equipment
    """
    return set(fileStr.split(","))

def fileEquipmentSet2Str(equipment:set[str]) -> str:
    """file util function: convert a set of equipment to a a line can be saved in data file
    Args:
        equipment (set[str]): a set of string representing equipment
    Returns:
        str: comma-splitted line contains each equipment in set
    """
    return ",".join(str(e) for e in equipment)


def fileTimeSlot2Str(ts) -> str:
    """convert this TimeSlot object to a string
        which keeps all information of this object.
        The string can be later used to reversely make 
        the same TimeSlot object using fileStr2TimeSlot() function.

    Returns:
        str: a string contains all the information of this object.
        for example:
            timeSlot from   January 4th 2022. 08:30 (quarter 2)
                        to  January 6th 2022. 18:00 (quarter 0)
            would have following output
                08.2-01/04/2022__18.0-01/06/2022
    """
    head = ts.get_head()
    hh = head.getHour()
    qh = head.getQuarter()
    dh = head.getDate()
    hs = f"{hh:02}.{qh}-{dh:%m/%d/%Y}"

    tail = ts.get_tail()
    ht = tail.getHour()
    qt = tail.getQuarter()
    dt = tail.getDate()
    ts = f"{ht:02}.{qt}-{dt:%m/%d/%Y}"
            
    return hs+"__"+ts

def fileStr2TimeSlot(tsStr:str):
    from TimeSlot import TimeSlot
    from TimeSlot import TimePoint
    """reverse operation for fileTS2Str(), which takes a
        formatted string and convert to a TimeSlot object.

    Args:
        tsStr (str): example:
            a string of:
            08.2-01/04/2022__18.0-01/06/2022    
        would have
    Returns:
            TimeSlot: 
                from    January 4th 2022. 08:30 (quarter 2)
                to      January 6th 2022. 18:00 (quarter 0)     
    """
    dateFormat = "%m/%d/%Y"
    (strHead, strTail) = tsStr.split("__")[:2]
    (strHeadTime, strHeadDate) = strHead.split("-")[:2]
    (strTailTime, strTimeDate) = strTail.split("-")[:2]
    headHour, headQuarter = (int(k) for k in (strHeadTime.split(".")[:2]))
    headDate = datetime.datetime.strptime(strHeadDate, dateFormat).date()
    tailHour, tailQuarter = (int(k) for k in (strTailTime.split(".")[:2]))
    tailDate = datetime.datetime.strptime(strTimeDate,dateFormat).date()
    
    headTimePoint, tailTimePoint = TimePoint(headHour, headQuarter, headDate), TimePoint(tailHour, tailQuarter, tailDate)
    parsed = TimeSlot(headTimePoint, tailTimePoint)
    return parsed

def fileAvailability2Str(availability) -> str:
    """from room's availability field to string
    comma-split all the time slots in the list

    Args:
        availability (list[TimeSlot]): 
            Availability attribute of Room,
            which is a list of TimeSlot objects

    Returns:
        str: comma-splitted string of timeslot objects
    """
    return ",".join(fileTimeSlot2Str(ts) for ts in availability)

def fileStr2Availability(avaStr:str) -> list:
    """from string in file to the availability attribute of Room object,
    the reverse-operation of fileAvailability2Str()
    Args:
        avaStr (str): comma-splitted string of timeslot objects 
            representing the availability
    Returns:
        list[TimeSlot]: list of available times for the room object.
    """
    return [fileStr2TimeSlot(ts) for ts in avaStr.split(",")]

def fileRoom2Str(room) -> str:
    """ convert this Room object to a string
        which keeps all information of this object.
        The string can be later used to reversely make 
            the same Room object using fileStr2Room() function.

    Args:
        room (Room): example: room{
            r.name = 'HL-212'; r.capacity = 7; r.location = Cameron Library South Wing Lower 2;
            r.equipment = {'blackboard', 'chalk', 'light'}
            r.availability = [TimeSlot from <17:30 01/04/2022> to <18:00 01/06/2022>, ...]}
        which would have
    Returns:
        str: 'HL-212, 7, Cameron Library South Wing Lower 2
                blackboard, chalk, light
                17.2-01/04/2022__18.0-01/06/2022, ...'
            (multiline str)
    """
    outStr = ""
    # first line data (id, capacity, location)
    outStr += (room.get_id() + ","
                + str(room.get_capacity())
                + "," + room.get_location() + "\n")
    
    # second line data (equipment)
    outStr += fileEquipmentSet2Str(room.get_equipment()) + "\n"

    # third line data (availability)
    outStr += fileAvailability2Str(room.get_availability())

    return outStr

def fileStr2Room(fileStr: str):
    """reverse operation of fileRoom2Str(), 
    which loads a room object from a string in the formatted file
    Args:
        fileStr (str): a formatted multiline string that contains the room object.
    Returns:
        Room: the output object.
    for examples, see fileRoom2Str()
    """
    from Room import Room

    (line1, line2, line3) = fileStr.split("\n")[:3]
    
    # first line data: (id, capacity, location)
    (name, capacity, location) = line1.split(",")[:3]
    capacity = int(capacity)

    # second line data: (equipment)
    equipment = fileStr2EquipmentSet(line2)

    # third line data: (availability)
    availability = fileStr2Availability(line3)

    return Room(name, capacity, location, equipment, availability)


def fileRoom2File(room, inDir = False) -> None:
    """write the data of one room to a file
    with filename = roomName
    
    Args:
        room (Room): a Room object
    """
    filePath = "Rooms\\"+room.get_id()+".txt"
    if inDir:
        filePath = room.get_id()+".txt"
    # open file and write the room data in file
    with open(filePath, "w") as writer:
        writer.write(
            fileRoom2Str(room)
        )
    return

def fileFile2Room(filename:str, inDir = False):
    """load a room object from the file
    given pathname

    Args:
        roomid (str): the id of room,
        which is also the filename of the file 

    Returns:
        Room: the room object described by the file
    """
    filePath = "Rooms\\"+filename
    if inDir:
        filePath = filename
    with open(filePath, "r") as reader:
        roomString = reader.read()
    return fileStr2Room(roomString)


def fileFile2RoomFromID(roomid:str, inDir=False):
    """load a room object from the file
    given pathname

    Args:
        roomid (str): the id of room,
        which is also the filename of the file 

    Returns:
        Room: the room object described by the file
    """
    filePath = "Rooms\\"+roomid+".txt"
    if inDir:
        filePath = roomid+".txt"
    with open(filePath, "r") as reader:
        roomString = reader.read()
    return fileStr2Room(roomString)

def fileReservation2Str(reservation):
    outStr = ""
    outStr += reservation.getName() + ", " + reservation.getContact() + "," + reservation.getRoomName()+"\n"
    outStr += fileTimeSlot2Str(reservation.getTimeSlot())
    return outStr

def fileStr2Reservation(inp):
    from Reservation import Reservation
    (line1, line2) = inp.split("\n")
    (name, contact, roomName) = line1.split(",")[:3]
    timeslot = fileStr2TimeSlot(line2)
    
    return Reservation(name, contact, roomName, timeslot)

def fileReservation2File(res, inDir= False):
    name = ""
    name += res.getName().strip(" ")+"_"+res.getRoomName()+"_"
    name += res.getTimeSlot().get_head().strName()
    
    filePath = "Reservations\\"+name+".txt"
    if inDir:
        filePath = name+".txt"
    # open file and write the room data in file
    with open(filePath, "w") as writer:
        writer.write(
            fileReservation2Str(res)
        )
    return


def fileFile2Reseration(fileName, inDir=False):
    filePath = "Reservations\\"+fileName
    if inDir:
        filePath = fileName
    with open(filePath, "r") as reader:
        resString = reader.read()
    return fileStr2Reservation(resString)


def allRoomNameInDir() -> list[str]:
    """get all room names in directory
    Returns:
        list[str]: list of room names
    """
    import os
    return [filename.split(".txt")[0] for filename in os.listdir("Rooms")]



def filter_room(roomList: list, equipment: set[str] = {}, 
                location: str = "", capacity: int = -1, availability: list = []) -> list:
                
    """filter the list of inputed rooms to return only the rooms that match the conditions
    Args:
        roomList (list[Room]): Input of available rooms
        equipment (set[str]): Required equipment. None by default
        location (str): location of the room. empty by default
        capacity (int): minimium capacity of the room. no requirement by default
        availability (list[TimeSlot]): a list of required time slots that room need to be available. None by default
    Returns:
        list[Room]: a list of Room objects that match the conditions.
    """
    filtered = []

    for room in roomList:
        isValidPlace = False
        # Testing for equipment
        if equipment.issubset(room.get_equipment()):
            # Testing for location
            if (location == room.get_location()) or (len(location==0)):
                # Testing for capacity
                if capacity <= room.get_capacity():
                    isValidPlace = True
                    # Testing for availability
                    isFreeOnDemand = True
                    for timeslot in availability:
                        if not room.availiableAt(timeslot):
                            isFreeOnDemand = False
        if isValidPlace and isFreeOnDemand:
            filtered.append(room)
    return filtered


def findRoomByName(searchName:str, roomList: list) -> list:
    matchingRooms = []
    
    for room in roomList:
        if searchName in room.name:
            matchingRooms.append(room)
    return matchingRooms