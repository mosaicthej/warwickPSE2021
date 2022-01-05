import datetime
class TimePoint:
    pass
class TimeSlot:
    pass


class TimePoint:
    def __init__(self, hour:int, quarter:int, date:datetime.date):
        self.hour = hour
        self.quarter = quarter
        self.date = date

    def next(self) -> TimePoint:
        """
        Returns:
            TimePoint: TimePoint at next quarter
        """
        if not self.quarter == 3:
            return TimePoint(self.hour, self.quarter+1, self.date)
        else: # quarter == 3
            if not self.hour == 23:
                return TimePoint(self.hour+1, 0, self.date)
            else: # hour == 23
                return TimePoint(0, 0, self.date + datetime.timedelta(days=1)) 
    
    def previous(self) -> TimePoint:
        """
        Returns:
            TimePoint: TimePoint at previous quarter
        """
        if not self.quarter == 0:
            return TimePoint(self.hour, self.quarter-1, self.date)
        else: # if quarter is 0, borrow from previous hour
            if not self.hour == 0:
                return TimePoint(self.hour-1, 3, self.date)
            else: # if hour also 0, borrow from previous dat
                return TimePoint(23, 3, self.date + datetime.timedelta(days=1))


    # for comparsions
    def __eq__(self, o: TimePoint) -> bool:
        return (self.hour == o.hour) and (self.quarter == o.quarter) and (self.date == o.date)

    def __ne__(self, o:TimePoint) -> bool:
        return (not(self.__eq__(o)))

    def __lt__(self, o: TimePoint) -> bool:
        lt = False
        if self.date < o.date:
            lt = True
        elif (self.date == o.date) and (self.hour < o.hour):
            lt = True
        elif (self.date == o.date) and (self.hour == o.hour) and (self.quarter < o.quarter):
            lt = True
        return lt

    def __le__(self, o: TimePoint) -> bool:
        return (self.__eq__(o) or self.__lt__(o))

    def __gt__(self, o: TimePoint) -> bool:
        return not(self.__lt__(o) or self.__eq__(o))

    def __ge__(self, o: TimePoint) -> bool:
        return self.__gt__(o) or self.__eq__(o)

    # getters
    def getHour(self) -> int:
        return self.hour
    
    def getQuarter(self) -> int:
        return self.quarter
    
    def getMinute(self) -> int:
        return 15*self.quarter
    
    def getDate(self) -> datetime.date:
        return self.date

    def __str__(self) -> str:
        # return "TimePoint at " + str(self.date) +"-"+ str(self.hour) +":"+ str(self.quarter*15)
        return f"TimePoint at {self.date:%Y-%m-%d} {self.hour:02}:{self.quarter*15:02}"



class TimeSlot:
    def __init__(self, beginTime:TimePoint, endTime: TimePoint) -> TimeSlot:
        self.beginTime = beginTime
        self.endTime = endTime

    def hasConflicts(self, other: TimeSlot) -> bool:
        """
        checking if this timeslot has conflict with another

        Args:
            other (TimeSlot): Another TimeSlot object

        Returns:
            bool:
             true if either:
                other.endTime is after this.beginTIme
                or
                other.beginTime is before this.endTime

        """
        return (other.endTime > self.beginTime) or (other.beginTime < self.endTime)

    def canFit(self, fitter:TimeSlot) -> bool:
        """check to see if another TimeSlot object can fit in this TimeSlot
             if true, then should be able to book for this slot.

        Args:
            taker (TimeSlot): The bigger time frame representing the availabile times can be booked.

        Returns:
            bool: true if can be booked.
        """
        return (fitter.beginTime >= self.beginTime) and (fitter.endTime <= self.endTime)


    def takeAway(self, taker:TimeSlot) -> list[TimeSlot]:
        """Take a period of time away from the current timeslot,

        Args:
            taker(TimeSlot): The lesser timeslot which will takeaway from current

        Returns:
            list[TimeSlot]: List of (usually 2) new timeslot fragments. (resulting from taken away in middle)
            if a conflict is created (not fitting the bigger timeframe)
        """
        fragments = []
        if not self.canFit(taker):
            # if not fitting, append self to the fragments
            # no fit -> no book -> no change
            print("no fit!")
            fragments.append(self)
        else:
            if taker.beginTime > self.beginTime:
                # if there are spaces between the heads
                # append the space between heads to the fragments
                fragments.append(TimeSlot(self.beginTime, taker.beginTime))
            if taker.endTime < self.endTime:
                # if there are spaces between the tails
                # append the space between tails to fragments
                fragments.append(TimeSlot(taker.endTime, self.endTime))
        return fragments

    def contains(self, timepoint:TimePoint) -> bool:
        """check if timepoint is inside this time slot
        Args:
            timepoint (TimePoint): a timepoint object
        Returns:
            bool: true if timepoint is inside this time slot.
        """
        return (timepoint<= self.beginTime
            and timepoint<= self.endTime)
    

    def timePointsAfter(self, startTime:TimePoint) -> List[TimePoint]:
        """
        Args:
            startTime (TimePoint): where to start count
        Returns:
            List[TimePoint]: List of all timepoints before end of this slot.
        """
        timePointsList = []
        while startTime < self.endTime:
            tps.append(startTime)
            startTime = startTime.next()
        return timePointsList


    def get_head(self) -> TimePoint:
        """getter for the head of the timeslot

        Returns:
            TimePoint: point where the timeSlot begins
        """
        return self.beginTime

    def get_tail(self) -> TimePoint:
        """getter for the tail of the timeslot

        Returns:
            TimePoint: point where the timeSlot ends
        """
        return self.endTime


    def __str__(self) -> str:
        return "timeslot from: "+str(self.beginTime)+" to "+str(self.endTime)

    def __eq__(self, other) -> bool:
        return (self.beginTime == other.get_head()
            and self.endTime == other.get_tail())