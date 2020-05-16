from data import Data
import api_details as api
import speech_recognition as sr 
import re



data = Data(api.API_KEY, api.PROJECT_TOKEN)


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
#audio = get_audio()
#print(audio)

print(data.get_most('tests'))
#print(data.data)