from Event import Event

class EventController:
    def __init__(self):
        pass
    
    @staticmethod
    def createEvent(None, user_id, name, description, location, start_time, end_time, tags, is_private, invite_list):
        event = Event(user_id, name, description, location, start_time, end_time, tags, is_private, invite_list)
        event_id = DAO.insertEvent(event)
        for invitee in invite_list:
            EventController.sendInvite(event_id, invitee)
        CalendarController.addEvent(event_id, user_id)
    
    @staticmethod
    def sendInvite(event_id, user_id):
        CalendarController.addEvent(event_id, user_id, True)