#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
import requests

from viewstate import VIEWSTATE

SCHEDULE_URL = "http://nextride.brampton.ca/mob/SearchBy.aspx"
VIEWSTATE_FIELD = "__VIEWSTATE"
STOP_FIELD = "ctl00$mainPanel$searchbyStop$txtStop"
REALTIME_FIELD = "ctl00$mainPanel$btnGetRealtimeSchedule"
REALTIME_VALUE = "GO"
STOP_DESC_ELEMENT = "ctl00_mainPanel_lblStopDescription"
SEARCH_RESULT_ELEMENT = "ctl00_mainPanel_gvSearchResult"

def scrape(stop):
    return parse(request(stop))

def request(stop):
    payload = {
        VIEWSTATE_FIELD: VIEWSTATE,
        STOP_FIELD: stop,
        REALTIME_FIELD: REALTIME_VALUE
    }
    resp = requests.post(SCHEDULE_URL, data=payload)
    return resp

def parse(response):
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find(id="ctl00_mainPanel_lblError"):
        return None

    if soup.find(id=STOP_DESC_ELEMENT):
        stop_desc = soup.find(id=STOP_DESC_ELEMENT)
        stop_id = stop_desc.string.split(", ", 1)[0].replace("Stop ", "")
        stop_name = stop_desc.string.split(", ", 1)[1].replace(" at ", " / ")
    if soup.find(id=SEARCH_RESULT_ELEMENT):
        buses = soup.find(id=SEARCH_RESULT_ELEMENT).find_all("tr")
        schedule = {"stopID": stop_id, "stopName": stop_name}
        if buses[1].td.string == "No Service":
            schedule.update(routes=None)
        else:
            routes = []
            for bus in buses[1:]:
                route = bus.td.string.split(" to ", 1)
                time = bus.td.next_sibling.string
                routes.append({"route": route[0].replace("Route ", ""), "direction": route[1], "time": time})
            schedule.update(routes=routes)
    return schedule


if __name__ == "__main__":
    stop = "2000"
    schedule = scrape(stop)
    print(json.dumps(schedule, indent=4))
