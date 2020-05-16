from data import Data
import api_details as api
import speech_recognition as sr 
import re
from clear import clear
import time

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

def deaths(text, data):
    for country in data.country_list:
        if country in text:
            countrydata = data.get_country_data(country)['deaths']
            
            return f'{country.title()} has had {countrydata} deaths from coronavirus'
    
def tests(text, data):
    for country in data.country_list:
        if country in text:
            countrydata = data.get_country_data(country)['tests']
            
            return f'{countrydata} people have been tested for coronavirus in {country}'

def population(text, data):
    for country in data.country_list:
        if country in text:
            countrydata = data.get_country_data(country)['population']
            
            return f'{country} has a population of {countrydata}'

def cases(text, data):
    for country in data.country_list:
        if country in text:
            countrydata = data.get_country_data(country)['cases']
            
            return f'{countrydata} people have tested positive for coronavirus in {country}'
    
def main():

    data = Data(api.API_KEY, api.PROJECT_TOKEN)

    ENDWORD = 'exit'
    
    TOTAL_PATTERNS = {
        re.compile('[\w\d\s]+total+[\w\d\s]+deaths'):data.get_total_deaths,
        re.compile('total+[\w\d\s]+deaths'):data.get_total_deaths,
        re.compile('[\w\d\s]+worldwide+[\w\d\s]+deaths'):data.get_total_deaths,
        re.compile('[\w\d\s]+deaths+[\w\d\s]+world'):data.get_total_deaths,
        re.compile('[\w\d\s]+died+[\w\d\s]+world'):data.get_total_deaths,
        re.compile('[\w\d\s]+world+[\w\d\s]+died'):data.get_total_deaths,

        re.compile('[\w\d\s]+total+[\w\d\s]+cases'):data.get_total_cases,
        re.compile('total+[\w\d\s]+cases'):data.get_total_cases,
        re.compile('[\w\d\s]+worldwide+[\w\d\s]+cases'):data.get_total_cases,
        re.compile('[\w\d\s]+cases+[\w\d\s]+world'):data.get_total_cases,

        re.compile('[\w\d\s]+total+[\w\d\s]+recoveries'):data.get_total_recovered,
        re.compile('total+[\w\d\s]+recoveries'):data.get_total_recovered,
        re.compile('[\w\d\s]+world+[\w\d\s]+recovered'):data.get_total_recovered,
        re.compile('[\w\d\s]+recovered+[\w\d\s]+world'):data.get_total_recovered,
    }

    SELECT_PATTERNS = {
        re.compile('[\w\d\s]+deaths+[\w\d\s]'): deaths,
        re.compile('[\w\d\s]+died+[\w\d\s]'): deaths,
        re.compile('[\w\d\s]+died'): deaths,
        re.compile('[\w\d\s]+tests+[\w\d\s]'): tests,
        re.compile('[\w\d\s]+population+[\w\d\s]'): population,
        re.compile('[\w\d\s]+cases+[\w\d\s]'): cases,
        re.compile('[\w\d\s]+tested+[\w\d\s]+positive+[\w\d\s]'): tests,
        re.compile('[\w\d\s]+tested+[\w\d\s]+positive'): tests,
        re.compile('[\w\d\s]+tested+[\w\d\s]'): tests,
        re.compile('[\w\d\s]+tested'): tests,
    }

    while True:
        clear()
        print('I\'m listning...')
        text = get_audio()
        print(f'Question: {text}\n')
        
        result = None
        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
        
        if not result:
            for pattern, func in SELECT_PATTERNS.items():
                if pattern.match(text):
                    result = func(text, data)
                    break 
        if result:
            
            print(f'Answer {result}')
            
        if ENDWORD in text:
            break
        else:
            time.sleep(4)
        
if __name__ == '__main__':
    
    main()

