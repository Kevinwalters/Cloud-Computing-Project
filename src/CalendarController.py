class CalendarController:
    def __init__(self):
        pass
    
    @staticmethod
    def createCalendar(user_id):
        calendar = Calendar(None, user_id=user_id)
        calendar_id = DAO.saveCalendar(calendar)
    
    @staticmethod
    def addEvent(event_id, user_id, is_invite=False):
        calendar = CalendarController.getCalendar(user_id)
        if is_invite:
            calendar.invited_events.append(event_id)
        else:
            calendar.events.append(event_id)
            if event_id in calendar.invited_events:
                calendar.invited_events.remove(event_id)
        calendarJson = calendar.toJson()
        DAO.saveCalendar(calendar)
        
    @staticmethod
    def removeEvent(event_id, user_id):
        calendar = CalendarController.getCalendar(user_id)
        if event_id in calendar.events:
            calendar.events.remove(event_id)
        if event_id in calendar.invited_events:
            calendar.invited_events.remove(event_id)
        DAO.saveCalendar(calendar)
        
    @staticmethod
    def getCalendar(user_id):
        calendar = DAO.getCalendar(user_id)
        return calendar
    
    @staticmethod
    def removeCalendar(user_id):
        DAO.removeCalendar(user_id)