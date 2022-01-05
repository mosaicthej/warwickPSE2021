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
import Room
from TimeSlot import *
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

def fileTS2Str(ts:TimeSlot) -> str:
    """convert this TimeSlot object to a string
        which keeps all information of this object.
        The string can be later used to reversely make 
        the same TimeSlot object using fileStr2TS() function.

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

def fileStr2TS(tsStr:str) -> TimeSlot:
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
    "08.2-01/04/2022__18.0-01/06/2022"
    dateFormat = "%m/%d/%Y"
    (strHead, strTail) = tsStr.split("__")
    (strHeadTime, strHeadDate) = strHead.split("-")
    (strTailTime, strTimeDate) = strTail.split("-")
    headHour, headQuarter = (int(k) for k in (strHeadTime.split(".")))
    headDate = datetime.datetime.strptime(strHeadDate, dateFormat).date()
    tailHour, tailQuarter = (int(k) for k in (strTailTime.split(".")))
    tailDate = datetime.datetime.strptime(strTimeDate,dateFormat).date()
    
    headTimePoint, tailTimePoint = TimePoint(headHour, headQuarter, headDate), TimePoint(tailHour, tailQuarter, tailDate)
    parsed = TimeSlot(headTimePoint, tailTimePoint)
    return parsed


def fileRoom2Str(room:Room) -> str:
    """ convert this Room object to a string
        which keeps all information of this object.
        The string can be later used to reversely make 
            the same Room object using fileStr2Room() function.

    Args:
        room (Room): example:{
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
