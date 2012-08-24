import urllib
import urllib2

# Special thanks to 'mjv' (http://stackoverflow.com/users/166686/mjv) for http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python.

uri = 'http://nextride.brampton.ca/mob/Home.aspx'

#HTTP headers to simulate Mobile Safari on iPhone with iOS 5.1 and pass content type.
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Form fields and values in a list (any iterable, actually) of name-value tuples.  This helps with clarity and also makes it easy to later encoding of them.
formFields = (
   # Viewstate. May be fine to hardcode value, or may have to be refreshed each time / each day, by essentially running an extra page request and parse for this specific value.
   (r'__VIEWSTATE', r'/wEPDwUKLTcxOTEzNzI2NQ9kFgJmD2QWAgIDD2QWBGYPDxYCHgRUZXh0BSNCcmFtcHRvbiBUcmFuc2l0IE5leHQgUmlkZSAtIE1vYmlsZWRkAgIPZBYCAgEPZBYCZg9kFghmD2QWAgIBD2QWAgILD2QWAgIBD2QWAgIDDzwrAA0AZAICD2QWAgIBD2QWAmYPZBYEZg9kFgICCw9kFgwCAw8QZGQWAGQCBw8PFgIfAAUJOC8yNC8yMDEyZGQCCw8QZGQWAWZkAg0PEGRkFgFmZAIRDxBkZBYBAgpkAhMPEGRkFgECAWQCAQ9kFgICBQ88KwANAGQCAw9kFgICAQ9kFgICCw9kFgJmD2QWAmYPZBYCAgEPFgIeCWlubmVyaHRtbGVkAgQPZBYCAgEPZBYCAgMPZBYCAgEPFgIfAAXLBw0KcGFnZSAxDQogICAgPHA+DQogICAgICAgIFRoaXMgaXMgZmlyc3QgaGVscCBwYWdlLiBDbGljayA8YSBpZD0ibGluazEiIGhyZWY9ImphdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCdjdGwwMCRtYWluUGFuZWwkTW9iTWFpblBhbmVsMSRNb2JIZWxwQm94MSRoZWxwUGFuZWwnLCdQYWdlMS5odG0nKSI+aGVyZTwvYT4gdG8gZ28gdG8gbmV4dC48L3A+DQogICAgICA8cD4gIFRoaXMgaXMgZmlyc3QgaGVscCBwYWdlLiBDbGljayA8YSBpZD0iQTEiIGhyZWY9ImphdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCdjdGwwMCRtYWluUGFuZWwkTW9iTWFpblBhbmVsMSRNb2JIZWxwQm94MSRoZWxwUGFuZWwnLCdwYWdlIDIuaHRtJykiPmhlcmU8L2E+IHRvIGdvIHRvIG5leHQuPC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgZHNhZHNhPC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgJm5ic3A7PC9wPg0KICAgIDxwPiAgcnJld3JldzwvcD4NCg0KZBgFBTljdGwwMCRtYWluUGFuZWwkTW9iTWFpblBhbmVsMSRNb2JSZWFsVGltZTEkZ3ZTZWFyY2hSZXN1bHQPZ2QFOWN0bDAwJG1haW5QYW5lbCRNb2JNYWluUGFuZWwxJE1vYlNjaGVkdWxlMSRndlNlYXJjaFJlc3VsdA9nZAU1Y3RsMDAkbWFpblBhbmVsJE1vYk1haW5QYW5lbDEkTW9iU2NoZWR1bGUxJG12U2NoZWR1bGUPD2RmZAUwY3RsMDAkbWFpblBhbmVsJE1vYk1haW5QYW5lbDEkTXVsdGlWaWV3TWFpblBhbmVsDw9kZmQFPGN0bDAwJG1haW5QYW5lbCRNb2JNYWluUGFuZWwxJE1vYlJlYWxUaW1lMSRNdWx0aVZpZXdSZWFsVGltZQ8PZGZkMqrWzxYId4QZ3RNOjWySh5W31cA='),

   # Fields of interest: search criteria
	(r'ctl00$lbtnHome', 'Home'),
	(r'ctl00$mainPanel$MobMainPanel1$MobRealTime1$txtStop', '1000'),
	(r'ctl00$mainPanel$MobMainPanel1$MobRealTime1$btnGO', 'GO'),
)

# Encode fields
encodedFields = urllib.urlencode(formFields)

# POST Request
req = urllib2.Request(uri, encodedFields, headers)
html = urllib2.urlopen(req)

# Store contents of HTML page in text file for parsing later.

try:
  fout = open('response.html', 'w')
except:
  print('Could not open output file.\n')

fout.writelines(html.readlines())
fout.close()
