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
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

model_name = 'sshleifer/distilbart-cnn-12-6'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

import nltk
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from newspaper import Article
from nltk.tokenize import sent_tokenize
from summa.summarizer import summarize
from transformers import pipeline

nltk.download("punkt")


#from udemyscraper import UdemyCourse

DATA_BASE_NAME = "fin_data.db"
TABLE_NAME = "word_definition"
EXTRACT_FIELD = "Word_definition"
KEY_WORD = "Word"

from docquery import document, pipeline
p = pipeline('document-question-answering')
doc = document.load_document("/home/ubuntu/STT_Hackathon/webscraping/src/question_answering/invoice.png")

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
        print(r.json())
        try:
            if r.json():
                return (r.json()['result'][0]['number'])
            else:
                return("Unable to create Incident")
        except Exception as e:
            return("Unable to create Incident")
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
                dispatcher.utter_message(text='Created a help desk ticket for you here is the ticket number\n Ticket Number :'+str(inc_number))
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
            dispatcher.utter_message(text='please mention one of the following operations in your query\n1.Create, \n2.Update, \n3.Delete')
        return []




class DocumentDetails(Action):

    def name(self) -> Text:
        return "documentdetails_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        doc_key = next(tracker.get_latest_entity_values("keys"), None)
        doc_question = tracker.latest_message["text"]
        print(doc_question)
        if not doc_question:
            msg = f"Could not get required details from the document"
            dispatcher.utter_message(text=msg)
            return []
        
        answer = p(question=doc_question, **doc.context)['answer']

        print('information extracted from the document : ', answer)

        if answer:
            if doc_key:
                dispatcher.utter_message(text=str(doc_key)+ ' is '+str(answer))
            else:
                dispatcher.utter_message(str(answer))
        else:
            dispatcher.utter_message(text="Could not get details from the document")
        return []

class FinanceDomain(Action):

    def name(self) -> Text:
        return "financedomain_response"

    def get_news(self, stock, n_results):
        header_gen = Headers(headers=True)
        headers = header_gen.generate()
        params = {"q": stock + " stock news"}
        response = requests.get(
            "https://news.google.com/search", headers=headers, params=params
        )
        soup = BeautifulSoup(response.text, "lxml")
        url_elems = soup.find_all(class_="VDXfz")
        urls = []
        for elem in url_elems:
            urls.append("https://news.google.com" + elem["href"][1:])
        articles = []
        total_results = 0
        for url in urls:
            if total_results == n_results:
                break
            try:
                article = Article(url)
                article.download()
                article.parse()
                article = article.text
                if len(article.split()) > 50:
                    articles.append(article)
                    total_results += 1
            except:
                continue
        return articles

    def gen_corpus(self, articles, stock, length):
        raw_corpus = ""
        for article in articles:
            article_sent = sent_tokenize(article)
            for sent in article_sent:
                if len(sent.split()) > 5 and stock.lower() in sent.lower():
                    raw_corpus += sent
        corpus = summarize(raw_corpus, words=length)
        return corpus


    def gen_summary(self, corpus, length):
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        min_length = int(0.8 * length)
        max_length = int(1.2 * length)
        raw_summary = summarizer(
            corpus[:1024], min_length=min_length, max_length=max_length
        )[0]["summary_text"]
        summary_sent = sent_tokenize(raw_summary)
        summary = ""
        for sent in summary_sent:
            summary += f"-{sent}\n"
        return summary


    def gen_sentiment(self, corpus):
        analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        raw_sentiment = analyzer(corpus[:512], return_all_scores=True)
        sentiment = {}
        for sentiment_dict in raw_sentiment[0]:
            label = sentiment_dict["label"]
            value = sentiment_dict["score"]
            if label == "positive":
                label = "bull"
            elif label == "negative":
                label = "bear"
            else:
                label = "neutral"
            sentiment[label] = value
        return sentiment

    def gen_report(self, stock, length):
        news = self.get_news(stock, length / 5)
        corpus = self.gen_corpus(news, stock, length * 5)
        summary = self.gen_summary(corpus, length)
        sentiment = self.gen_sentiment(corpus)
        return summary, sentiment

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        print("Here for stock price")
        asserts = next(tracker.get_latest_entity_values("asserts"), None)
        input_text = tracker.latest_message["text"]
        #print(f"NLP word definition:{asserts}")
        print(asserts)
        if 'trend' in input_text.lower():
            try:
                print('came to try')
                dispatcher.utter_message(text='Analysing...., Please wait')
                summary, sentiment = self.gen_report(asserts, 100)
                dispatcher.utter_message(text='Here is the summary I have brought you from my analysis:\n'+str(summary)+'\nand also here is my intution over market trend:\n'+str(max(sentiment, key=sentiment.get)))
            except Exception as e:
                print('came to except')
                dispatcher.utter_message(text='Unable to get you summary for this stock, try with any other stock\n'+ e)
            return []
        else:
            try:
                data = yf.Ticker(asserts.upper())
            except Exception as e:
                dispatcher.utter_message(text='Unable to get you summary for this stock, try with any other stock')
                return []
            if 'currentPrice' in data.info.keys():
                current_price = data.info['currentPrice']
            elif 'navPrice' in data.info.keys():
                current_price = data.info['navPrice']
            else:
                dispatcher.utter_message(text='Unable to get you summary for this stock, try with any other stock')
                return []

        if current_price:
            dispatcher.utter_message(text='Current price of '+ asserts +' is '+str(current_price))
        else:
            dispatcher.utter_message(text='Unable to get you summary for this stock, try with any other stock')
        return []


# class ActionService(Action):
#     def name(self) -> Text:
#         return "action_service"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         buttons= [
#             {"payload":'/docs{"content_type":"blogs"}',"title":"Documenation"},
#             {"payload":'/video{"content_type":"video"}',"title":"Video content"}
#         ]
#         dispatcher.utter_message(text="How would you like to learn with?", buttons=buttons)
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "definition_response"

    def get_definition(self, word_def):
        current_path = os.getcwd()
        db_file_path = os.path.join(current_path,"..","db",DATA_BASE_NAME)
        con = sqlite3.connect(db_file_path)
        cur = con.cursor()
        sql_query = f"""SELECT {EXTRACT_FIELD} from {TABLE_NAME} WHERE UPPER({KEY_WORD}) LIKE UPPER("{word_def}");"""
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

class Summarization(Action):

    def name(self) -> Text:
        return "summarization"

    def summarize(self, inp):
        inp = inp.replace('\n','')
        inp = tokenizer.encode(inp, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(inp, num_beams=2, min_length=50, max_length=120, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        #print("Here for stock price")
        #asserts = next(tracker.get_latest_entity_values("asserts"), None)
        input_text = tracker.latest_message["text"]
        #print(f"NLP word definition:{asserts}")

        if not input_text:
            msg = f"Could not get required details"
            dispatcher.utter_message(text=msg)
            return []
        summarized_text = self.summarize(input_text)

        
        if summarized_text:
            dispatcher.utter_message(text=str(summarized_text))
        else:
            dispatcher.utter_message(text="Could not get summarized text")
        return []

class CoursesRecommendation(Action):

    def name(self) -> Text:
        return "courses_recommendation"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("This is executing run function")
        #print("Here for stock price")
        domain = next(tracker.get_latest_entity_values("domain"), None)
        #input_text = tracker.latest_message["text"]
        #print(f"NLP word definition:{asserts}")
        
        try:
            course = UdemyCourse()
            course.fetch_course(domain)
        except Exception as e:
            dispatcher.utter_message(text="Could not get required details")
            return []

        if not course.title:
            msg = f"Could not get required details"
            dispatcher.utter_message(text=msg)
            return []
        else:
            dispatcher.utter_message(text='Here is a recommendation for you from udemy :\n'+course.title)
        return []


class ActionCarousel(Action):

    def name(self) -> Text:
        return "action_carousel"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('came to action carousel')
        message = {
            "type" : "template",
            "payload" : {
                "template_type" : "generic",
                "elements" : [
                    {
                        "title" : "Finance Q&A",
                        "subtitle" : "Service 1",
                        "image_url" : "https://lh4.googleusercontent.com/ejtOj2bNy0vgoRimwNAd3P50jzo_cuwQfgo7ay68NABYpfFPKgJBUH0pqByfwzvkhqg=w2400",
                        "buttons" : [
                            {
                            "title" : "Ask question",
                            "payload" : "get_definition",
                            "type" : "postback"
                            }
                        ]
                    },
                    {
                        "title" : "Summarization",
                        "subtitle" : "Service 2",
                        "image_url" : "https://lh5.googleusercontent.com/qBi-XBzUXWT4uEOnnX97HgvtcLmROlc38icwhICcrj79rz3utuz29tR8RLWkU-1p7X8=w2400",
                        "buttons" : [
                            {
                            "title" : "Summarize",
                            "payload" : "get_summarize",
                            "type" : "postback"
                            }
                        ]
                    },
                    {
                        "title" : "Service Now ticketing",
                        "subtitle" : "Service 3",
                        "image_url" : "https://lh6.googleusercontent.com/4qeSfw5pb2B6VKmY4iARnLD-p6gHktzeAUTSY_kgfrdnktYt6l0enKoifV_7R2UuyXM=w2400",
                        "buttons" : [
                            {
                            "title" : "Raise a ticket",
                            "payload" : "get_snow",
                            "type" : "postback"
                            }
                        ]
                    },
                    {
                        "title" : "Document extraction",
                        "subtitle" : "Service 4",
                        "image_url" : "https://lh6.googleusercontent.com/1N_yMztdf--ueR8xtH-OzHLHrCEt0qFZfrYirpujv3PhsugqXcd2EPIKZ5u2tN3wEqQ=w2400",
                        "buttons" : [
                            {
                            "title" : "Extract",
                            "payload" : "get_doc_det",
                            "type" : "postback"
                            }
                        ]
                    },
                    {
                        "title" : "Stocks Market",
                        "subtitle" : "Service 4",
                        "image_url" : "https://lh6.googleusercontent.com/ENifr3AaHm2py1xsLqS069BxH-zAWjRQNcm-AqpoVtOfPpUEMPgHc7qpG7KAv-PyGIA=w2400",
                        "buttons" : [
                            {
                            "title" : "Get stock details",
                            "payload" : "get_finance_det",
                            "type" : "postback"
                            }
                        ]
                    },
                    {
                        "title" : "Courses Recomendation",
                        "subtitle" : "Service 4",
                        "image_url" : "https://lh5.googleusercontent.com/qBi-XBzUXWT4uEOnnX97HgvtcLmROlc38icwhICcrj79rz3utuz29tR8RLWkU-1p7X8=w2400",
                        "buttons" : [
                            {
                            "title" : "Recomend me courses",
                            "payload" : "get_courses_rec",
                            "type" : "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(text="Below are the services which I can help you with")
        dispatcher.utter_message(attachment=message)
        
        return []