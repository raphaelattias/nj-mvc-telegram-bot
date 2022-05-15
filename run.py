from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from simple_parsing import ArgumentParser

from utils import send_text, send_location

earliest_location = 'Newark'
earliest_time = 0

parser = ArgumentParser()
parser.add_argument("--token", type=str, default=None, help="Your telegram bot API token, e.g: 0000000000:aaaaaaaaaaaaaaaaaa")
parser.add_argument("--userid", type=str, default=None, help="Your personal telegram USER ID, e.g: 0000000000")
parser.add_argument("--permit", type=str, default="knowledge", help="The test you want to pass, can be either 'knowledge' or 'initial'.")
parser.add_argument('-f', action='append', default = [], \
  help = "List of locations to filter. e.g: -f Camden -f West Deptford -f Salem")

args = parser.parse_args()
TOKEN = args.token
USERID = args.userid
PERMIT = args.permit
filtered_locations = args.f

#filtered_locations = ['Camden','West Deptford', 'Salem','Vineland','Cardiff', 'Rio Grande', 'Wayne', 'Toms River']
if not TOKEN:
  TOKEN = input("token: ")
if not USERID:
  USERID = input("userid: ")
if not PERMIT:
  PERMIT = input("permit: ")

try:
  if PERMIT == 'initial':
    URL = 'https://telegov.njportal.com/njmvc/AppointmentWizard/15'
  elif PERMIT == 'knowledge':
    URL = 'https://telegov.njportal.com/njmvc/AppointmentWizard/19'
  else:
    raise ValueError(f"--permit should be either 'knowledge' or 'initial', input was {PERMIT}")
except ValueError:
  exit('Could not complete request.')


print("Search in progress.")

while True:
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(class_="text-capitalize")
  text = soup.find_all('script',type="text/javascript")[1].text
  myJson = json.loads(text.split('var locationData = ')[1].split(';\r\n        var')[0])

  locations = ['Bakers Basin',
  'Bayonne',
  'Camden',
  'Cardiff',
  'Delanco',
  'Eatontown',
  'Edison',
  'Elizabeth',
  'Flemington',
  'Freehold',
  'Lodi',
  'Newark',
  'North Bergen',
  'Oakland',
  'Paterson',
  'Rahway',
  'Randolph',
  'Rio Grande',
  'Salem',
  'South Plainfield ',
  'Toms River',
  'Vineland',
  'Wayne',
  'West Deptford']


  id_to_location = dict(zip([item['LocAppointments'][0]['LocationId'] for item in myJson], [item['Name'].split(' - ')[0] for item in myJson]))

  timedData = json.loads(text.split('var timeData = ')[1].split('\r\n ')[0])
  id_to_availability = {}

  for item in timedData:
    key = item['LocationId']
    try:
      id_to_availability[key] = item['FirstOpenSlot'].split(': ')[1].split(' ')[0]
    except IndexError:
      id_to_availability[key] = None 


  df = pd.DataFrame(id_to_availability.items(),index=id_to_availability.keys(), columns=['id','availability'])
  df.set_index('id', inplace=True)
  df.availability = pd.to_datetime(df.availability)
  df['location'] = df.apply(lambda x : id_to_location[int(x.name)], axis=1)
  
  if ((earliest_location != df.loc[df.availability.idxmin()].location) or (earliest_time != str(df.availability.min()).split(' ')[0])) and (df.loc[df.availability.idxmin()].location not in filtered_locations):
    earliest_location = df.loc[df.availability.idxmin()].location
    earliest_time = str(df.availability.min()).split(' ')[0]
    print(f"A new earliest location has been found. At {earliest_location}, NJ on the {earliest_time}.")

    message = f"A new earliest location has been found. At {earliest_location}, NJ on the {earliest_time}. Click here: {URL}."
    send_location(TOKEN=TOKEN, USERID=USERID,   location=earliest_location)
    send_text(TOKEN=TOKEN, USERID=USERID, message=message)

