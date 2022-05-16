import requests
from geopy.geocoders import Nominatim




def send_text(TOKEN, USERID, message="test"):

  # Create url
  url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

  # Create json link with message
  data = {'chat_id': USERID, 'text': message}

  # POST the message
  requests.post(url, data)

def send_location(TOKEN, USERID, location):
  loc = Nominatim(user_agent="GetLoc")
  getLoc = loc.geocode(f"{location} New Jersey")
  # Create url
  url = f'https://api.telegram.org/bot{TOKEN}/sendVenue'
  # Create json link with message
  data = {'chat_id': USERID, 'address': location, 'latitude': getLoc.latitude, 'longitude': getLoc.longitude,'title': location}
  # POST the message
  requests.post(url, data)

  


