from TimeSlot import *
from utils import *

# "declare" the classes just to bypass linter on annotations
class Room:
    pass

class Room:
    def __init__(self, id:str, capacity:int, location:str, 
        equipment:set[str], availability: list[TimeSlot]) -> Room:
        """make a new Room object
        Args:
            id (str): Room id or number, used to identify a room
            capacity (int): max people can be in the room
            equipment (tuple[str]): a list of equipments that the room contains
            location (str): location of the room (which building/ which floor/ etc.)
            availability (list[TimeSlot]): a sorted list of TimeSlots that represent when this is able to book.
        """
        self.id = id
        self.capacity = capacity
        self.equipment = equipment
        self.location = location
        self.availability = availability

    def bookAt(self, bookTime:TimeSlot) -> bool:
        """book at a given time.
            if successful, take the booked time away from availability.

        Args:
            bookTime (TimeSlot): The time period that user wishes to book

        Returns:
            bool: true if booked successfully.
        """
        i = self.availiableAt(bookTime)
        if i == -1:
            return False
        else:
            ava = self.availability[i]
            avaLeft = ava.takeAway(bookTime)
            if len(avaLeft) > 0: # if at least one side of the time still remains
                self.availability[i] = avaLeft[0]
            if len(avaLeft) > 1: # if both sides of the time remain
                self.availability.insert(i+1, avaLeft[1])
            self.__cleanUpAvailable() # clean up the lists (need to do everytime a operated on a list)
            return True

    def availiableAt(self, checkTime:TimeSlot) -> int:
        """checking if this room is available at given timeslot

        Args:
            checkTime (TimeSlot): The time period that going to be checked

        Returns:
            int: index that the available timeslot is among all availiable time of this room
                -1 if not availiable
        """
        for i in range(len(self.availability)):
            ava = self.availability[i]
            if ava.canFit(checkTime):
                return i
        return -1

    def __cleanUpAvailable(self) -> None:
        """cleaning up the list of availible times.
        (if two timeframe are consecutive, combine them.)
        """
        for i in range(1,len(self.availability)):
            thisTime = self.availability[i]
            prevTime = self.availability[i-1]
            if prevTime.get_tail() == thisTime.get_head():
                # if the tail of previous time matches the current time
                # combine the two into biggertime
                biggerTime = TimeSlot(prevTime.get_head(),thisTime.get_tail())

                # put biggerTime in place of the previous time
                self.availability[i-1] = biggerTime
                # remove the current time (since already combined in the biggerTime)
                self.availability.pop(i)


    # common getters

    def get_availability(self) -> list[TimeSlot]:
        """getting all the availability times for this room

        Returns:
            list[TimeSlot]: all availability timeSlots in a list.
        """
        return self.availability

    def get_id(self) -> str:
        return self.id

    def get_capacity(self) -> int:
        return self.capacity

    def get_equipment(self) -> set[str]:
        return self.equipment

    def get_location(self) -> str:
        return self.location

    def __eq__(self, other) -> bool:
        eq = True
        return (self.id == other.get_id()
            and self.equipment == other.get_equipment()
            and self.capacity == other.get_capacity()
            and self.location == other.get_location()
            and self.availability == other.get_availability())



# driver codes for testing purposes
dayBegin = TimePoint(0, 0, datetime.date.today())
# today
dayEnd = TimePoint(0,0, datetime.date.today() + datetime.timedelta(days=1))
# tomorrow

afternoonBegin = TimePoint(13, 0, datetime.date.today())
afternoonEnd = TimePoint(17,2, datetime.date.today())
afternoonPeriod = TimeSlot(afternoonBegin,afternoonEnd)

allDay = TimeSlot(dayBegin, dayEnd)

r = Room("SA-J", 15, "CCIS-L20", 
    {"light","blackboard","chalk"}, [allDay])
print(r.get_availability())

r.bookAt(afternoonPeriod)
print(r.get_availability())

r1 = Room("SA-K", 8, "CCIS-L2", 
    {"light","blackboard","chalk"}, [allDay])

r2 = Room("SA-F", 7, "CCIS-L2", 
    {"light","blackboard","chalk"}, [allDay])

for k in (r, r1, r2):
    fileRoom2File(k)
