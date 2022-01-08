class Reservation:
    def __init__(self, name, contact, roomName, timeslot):
        self.name = name
        self.contact = contact
        self.roomName = roomName
        self.timeSlot = timeslot

    def getName(self): return self.name
    def getContact(self): return self.contact
    def getRoomName(self): return self.roomName
    def getTimeSlot(self): return self.timeSlot
    
    