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
            new_event = Event("111111111111111111111111", name, description, loc, date, startTime, endTime, tags)
            events.append(new_event)
        print len(events)
        return events
    
        #TODO SAVE EVENTS