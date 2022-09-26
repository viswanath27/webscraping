# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os
import sqlite3
import requests
import yfinance as yf
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
