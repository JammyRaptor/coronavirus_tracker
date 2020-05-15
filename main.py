import requests
import api_details as api
import json
import pyttsx3
import speech_recognition as sr 
import re

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            'api_key': self.api_key
        }
        self.get_data()
    
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params = self.params)
        self.data = json.loads(response.text)

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']
    
    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']

    def get_country_data(self, country):
        data = self.data['countries']

        for content in data:
            if content['name'].lower() == country.lower():
                return content
        
        return '0'

data = Data(api.API_KEY, api.PROJECT_TOKEN)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('Exception:', str(e))
    
    return said.lower()
audio = get_audio()
print(audio)
speak(audio)