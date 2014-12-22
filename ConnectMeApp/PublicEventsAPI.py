from models import Event
import urllib2
import xml.etree.ElementTree as ET
import re


class PublicEventsAPI:
    rate_limit = float("inf")
    uri = "https://data.cityofnewyork.us/download/w3wp-dpdi/XML"
    
    def __init__(self):
        pass
       
    @staticmethod
    def queryAll():    
        response = urllib2.urlopen(PublicEventsAPI.uri)   
        resp = response.read()
        
        resp = re.sub(r'<event:', '<', resp)
        resp = re.sub(r'</event:', '</', resp)
        
        data = ET.fromstring(resp)
        events = list()
        
        data = data.find('channel')
        
        for event in data:
            if not event.tag == 'item':
                continue
            name=event.find('title').text
            description = event.find('description').text
            loc = event.find('location', namespaces=dict(event='event:')).text
            loc = event.find('coordinates').text
            loc_array = loc.split(',')
            lat = loc_array[0].strip()
            lng = loc_array[1].strip()
            category = event.find('categories').text
            if category:
                category = re.sub(r"\W\|\W", '|', category)
                tags = category.split('|')
                tags=filter(None,tags)
            else:
                tags = list()
            date = event.find('startdate').text
            date = re.sub('-', '', date)
            startTime = event.find('starttime').text
            endTime = event.find('endtime').text
            new_event = Event(user_id="111111111111111111111111", name=name, description=description, latitude=lat, longitude=lng, date=date, start_time=startTime, end_time=endTime, tags=tags)
            events.append(new_event)
        print len(events)
        for event in events:
            event.save()
        return events
    
        #TODO SAVE EVENTS