#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
import requests

from viewstate import VIEWSTATE

def rides(stop):
    payload = { '__VIEWSTATE': VIEWSTATE, 'ctl00$mainPanel$searchbyStop$txtStop': stop, 'ctl00$mainPanel$btnGetRealtimeSchedule': 'GO' }
    resp = requests.post('http://nextride.brampton.ca/mob/SearchBy.aspx', data=payload)
    return resp

def parse(response):
    soup = BeautifulSoup(response.text)
    if soup.find(id="ctl00_mainPanel_lblError"):
        return None

    if soup.find(id="ctl00_mainPanel_lblStopDescription"):
        stop_desc = soup.find(id="ctl00_mainPanel_lblStopDescription")
        stop_id = stop_desc.string.split(', ',1)[0].replace('Stop ','')
        stop_name = stop_desc.string.split(', ',1)[1].replace(' at ',' / ')
    if soup.find(id="ctl00_mainPanel_gvSearchResult"):
        buses = soup.find(id="ctl00_mainPanel_gvSearchResult").find_all('tr')
        schedule = {"stopID": stop_id, "stopName": stop_name}
        if buses[1].td.string == "No Service":
            schedule.update(routes=None)
        else:
            routes = []
            for bus in buses[1:]:
                route = bus.td.string.split(' to ',1)
                time = bus.td.next_sibling.string
                routes.append({"route": route[0].replace('Route ',''), "direction": route[1], "time": time})
            schedule.update(routes=routes)
    return schedule

if __name__ == "__main__":
    stop_id = "2000"
    schedule = parse(rides(stop_id))
    print json.dumps(schedule, indent=4)
