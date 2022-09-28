from textwrap import indent
import pysnow
import requests


def create_record(shor_descrpition, description):
    c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
    incident = c.resource(api_path='/table/incident')
    new_record = {
        'short_description': shor_descrpition,
        'description': description
    }
    result = incident.create(payload=new_record)
    r = requests.get(f"https://dev120493.service-now.com/api/now/table/incident?\
        short_description={shor_descrpition}&description={description}", auth=("admin", "m9*toMLZ^w9M"))
    print(r.json()['result'][0]['number'])
    if r.json():
        return (r.json()['result'][0]['number'])
    else:
        return("Incident not created successfully")

def retrieve_record():
    c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
    incident = c.resource(api_path='/table/incident')
    response = incident.get(query={'state': 1}, stream=True)
    for record in response.all():
        print(record['task_effective_number'])

def retrieve_first_record():
    c = pysnow.Client(instance='dev120493', user='myusername', password='m9*toMLZ^w9M')
    incident = c.resource(api_path='/table/incident')
    response = incident.get(query={'state': 3})
    print(response.first())


create_record("ejlktjlewjl", "lewrjtlj")
#retrieve_record()
#retrieve_first_record()