from models import Event
import urllib2
import xml.etree.ElementTree as ET
import re

#class that allows you to 
class PublicEventsAPI:
    rate_limit = float("inf")
    uri = "https://data.cityofnewyork.us/download/w3wp-dpdi/XML" #we use the NYC Special Events Public API
    
    def __init__(self):
        pass
       
    @staticmethod
    def queryAll():    
        response = urllib2.urlopen(PublicEventsAPI.uri)#make the query to the API
        resp = response.read()
        
        #there are some formatting issues when parsing, so do some replacements
        resp = re.sub(r'<event:', '<', resp)
        resp = re.sub(r'</event:', '</', resp)
        
        data = ET.fromstring(resp)
        events = list()
        
        data = data.find('channel')
        
        for event in data: #for each of the events:
            if not event.tag == 'item':
                continue
            name=event.find('title').text
            description = event.find('description').text
            loc = event.find('location', namespaces=dict(event='event:')).text
            loc = event.find('coordinates').text
            loc_array = loc.split(',')#latitude,longitude
            lat = loc_array[0].strip()
            lng = loc_array[1].strip()
            category = event.find('categories').text
            if category: #use the "category" to generate a list of tags
                category = re.sub(r"\W\|\W", '|', category) #tags | are | like | this
                tags = category.split('|')
                tags=filter(None,tags)
            else:
                tags = list()
            date = event.find('startdate').text
            date = re.sub('-', '', date)
            startTime = event.find('starttime').text
            endTime = event.find('endtime').text
            new_event = Event(user_id="111111111111111111111111", name=name, description=description, latitude=lat, longitude=lng, date=date, start_time=startTime, end_time=endTime, tags=tags)
            events.append(new_event) #create the new event, and append it to a list to be saved
        print len(events)
        for event in events:
            event.save()#save each of the events
        return events