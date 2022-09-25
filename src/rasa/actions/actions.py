# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import sqlite3
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "definition_response"

    def get_definition(self, word_def):
        con = sqlite3.connect("/Users/csot/rasa_bot/nlp_db.db")
        cur = con.cursor()
        sql_query = f"""SELECT nlp_definition from nlp_data WHERE nlp_key="{word_def}";"""
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
