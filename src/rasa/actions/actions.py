# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os
import sqlite3
import requests
import yfinance as yf
import pysnow
from textwrap import indent
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

DATA_BASE_NAME = "fin_data.db"
TABLE_NAME = "word_definition"
EXTRACT_FIELD = "Word_definition"
KEY_WORD = "Word"

from docquery import document, pipeline
p = pipeline('document-question-answering')
doc = document.load_document("/Users/csot/webscraping/src/question_answering/invoice-pwd.jpeg")

class ServiceNowActions(Action):

    def name(self) -> Text:
        return "snow_actions"
    

    def create_record(self, shor_descrpition, description):
        c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
        incident = c.resource(api_path='/table/incident')
        new_record = {
            'short_description': shor_descrpition,
            'description': description
        }
        result = incident.create(payload=new_record)
        r = requests.get(f"https://dev120493.service-now.com/api/now/table/incident?\
            short_description={shor_descrpition}&description={description}", auth=("admin", "m9*toMLZ^w9M"))
        print("First Instance number")
        print(r.json()['result'][0]['number'])
        if r.json():
            return (r.json()['result'][0]['number'])
        else:
            return("Incident not created successfully")

    # def retrieve_record():
    #     c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
    #     incident = c.resource(api_path='/table/incident')
    #     response = incident.get(query={'state': 1}, stream=True)
    #     print("Retriving other records")
    #     for record in response.all():
    #         print(record['task_effective_number'])

    def retrieve_first_record():
        c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
        incident = c.resource(api_path='/table/incident')
        response = incident.get(query={'state': 3}, stream=True)
        print("First Response")
        print(response.first())

    def update_record(self, update, incident_number):
        # Create client object
        c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
        # Define a resource, here we'll use the incident table API
        incident = c.resource(api_path='/table/incident')
        # Update 'short_description' and 'state' for 'INC0010019'
        try:
            updated_record = incident.update(query={'number': incident_number}, payload=update)
            return('Update of the incident is succesfull')
        except Exception as e:
            return('Update was not succesfull because of the following error \n'+str(e))

    def delete_record(self, incident_number):
        c = pysnow.Client(instance='dev120493', user='admin', password='m9*toMLZ^w9M')
        # Define a resource, here we'll use the incident table API
        incident = c.resource(api_path='/table/incident')

        # Delete incident with number 'INC0010001'
        try:
            result = incident.delete(query={'number': incident_number})
            return('Deletion of the incident is successfull')
        except Exception as e:
            return('Deletion of the incident is not successfull because of following error \n'+str(e))
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        short_description = next(tracker.get_latest_entity_values("sdec"), None)
        description = next(tracker.get_latest_entity_values("dec"), None)
        incident_number = next(tracker.get_latest_entity_values("inc"), None)
        input_text = tracker.latest_message["text"]
        
        print('short_description:',short_description)
        print('description:',description)
        print('incident_number:',incident_number)

        print(input_text)
        if 'create' in input_text.lower():
            if short_description or description:
                inc_number = self.create_record(short_description, description)
                dispatcher.utter_message(text=str(inc_number))
            else:
                dispatcher.utter_message(text='No information to create incident')


        elif 'update' in input_text.lower():
            if incident_number:
                update = {}
                if short_description:
                    update['short_description'] = short_description
                if description:
                    update['description'] = description
                if update:
                    result = self.update_record(update, incident_number)
                    dispatcher.utter_message(text=result)
                else:
                    dispatcher.utter_message(text='Update of incident is not succesful because of insufficient data')
            else:
                dispatcher.utter_message(text='Update of incident is not succesful because incident number is not mentioned')

        
        elif 'delete' in input_text.lower():
            if incident_number:
                result = self.delete_record(incident_number)
                dispatcher.utter_message(text=result)
            else:
                dispatcher.utter_message(text='Update of incident is not succesful because incident number is not mentioned')


        else:
            dispatcher.utter_message(text='please mention one of the following operations\n1.Create, 2.Update, 3.Delete')

        return []


# class ActionHaystack(Action):

#     def name(self) -> Text:
#         return "call_haystack"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         url = "http://localhost:8000/query"
#         payload = {"query": str(tracker.latest_message["text"])}
#         headers = {
#             'Content-Type': 'application/json',
#             'accept' : 'application/json'
#         }
#         response = requests.request("POST", url, headers=headers, json=payload).json()

#         if response["answers"]:
#             answer = response["answers"][0]["answer"]
#         else:
#             answer = "No Answer Found!"
#         print(f"answer:{answer}")
#         dispatcher.utter_message(text=answer)

#         return []

class DocumentDetails(Action):

    def name(self) -> Text:
        return "documentdetails_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        # doc_key = next(tracker.get_latest_entity_values("keys"), None)
        doc_question = tracker.latest_message["text"]
        print(doc_question)
        if not doc_question:
            msg = f"Could not get required details from the document"
            dispatcher.utter_message(text=msg)
            return []
        
        answer = p(question=doc_question, **doc.context)['answer']

        print('information extracted from the document : ', answer)

        if answer:
            dispatcher.utter_message(text=str(answer))
        else:
            dispatcher.utter_message(text="Could not get details from the document")
        return []

class FinanceDomain(Action):

    def name(self) -> Text:
        return "financedomain_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        print("Here for stock price")
        asserts = next(tracker.get_latest_entity_values("asserts"), None)
        #print(f"NLP word definition:{asserts}")
        print(asserts)
        if not asserts:
            msg = f"Could not get required details"
            dispatcher.utter_message(text=msg)
            return []
        data = yf.Ticker(asserts)
        current_price = data.info['currentPrice']
        #print(data.info['currentPrice'])

        if current_price:
            dispatcher.utter_message(text=str(current_price))
        else:
            dispatcher.utter_message(text="Could not get current price ")
        return []


class ActionService(Action):
    def name(self) -> Text:
        return "action_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons= [
            {"payload":'/docs{"content_type":"blogs"}',"title":"Documenation"},
            {"payload":'/video{"content_type":"video"}',"title":"Video content"}
        ]
        dispatcher.utter_message(text="How would you like to learn with?", buttons=buttons)
        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "definition_response"

    def get_definition(self, word_def):
        current_path = os.getcwd()
        db_file_path = os.path.join(current_path,"..","db",DATA_BASE_NAME)
        con = sqlite3.connect(db_file_path)
        cur = con.cursor()
        sql_query = f"""SELECT {EXTRACT_FIELD} from {TABLE_NAME} WHERE {KEY_WORD}="{word_def}";"""
        print(sql_query)
        result_proxy = cur.execute(sql_query)
        result_set = result_proxy.fetchall()
        print(result_set)
        if result_set:
            print(result_set[0][0])
            return result_set[0][0]
        else:
            return None


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        word_def = next(tracker.get_latest_entity_values("word_def"), None)
        print(f"NLP word definition:{word_def}")
        if not word_def:
            msg = f"Could not get definition"
            dispatcher.utter_message(text=msg)
            return []
        word_definition = self.get_definition(word_def)
        print(word_definition)
        if word_definition:
            dispatcher.utter_message(text=word_definition)
        else:
            dispatcher.utter_message(text="Could not get the word definition")
        return []
