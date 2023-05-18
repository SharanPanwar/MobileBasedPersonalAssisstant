
from __future__ import print_function
import os.path
from datetime import datetime
import speech_recognition as sr
import pyttsx3 
import webbrowser
import wikipedia
import wolframalpha
import os
import datetime
# from music import music
# from clap import Tester


# FileOpenAi = open('D:\Final Code-Minor Project\Report Content\APIKeys\openai.txt','r')
# apikey = FileOpenAi.read()
# FileOpenAi.close()

# from dotenv import load_dotenv
# import openai

# openai.api_key = apikey

# load_dotenv()
# completion = openai.Completion()

# # chat_log_template = '''You : Hello, who are you?
# # Computer : I am doing great. How can I help you today?
# '''



SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["Januraray", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]


# Speech engine initialisation
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
activationWord = 'computer' 
 
# Configure browser
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
 

# Wolfram Alpha client
appId = 'YL2324-JLKJGQ5TWK'
wolframClient = wolframalpha.Client(appId)
 
def speak(text, rate = 150):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
#     Tester()
# print("Hello, I am your personal assistant. How can I help you?")

 
def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')
 
    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)
 
    try: 
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en-in')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
 
    return query

def  wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
 
def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result received'
    try: 
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary
 
def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']
 
def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)
 
    if response['@success'] == 'false':
        return 'Could not compute'
    else:
        result = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listOrDict(pod1['subpod'])
            return result.split('(')[0]
        else: 
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0]
            speak('Computation failed. Querying universal databank.')
            return search_wikipedia(question)
        
    # Function to set an alarm
# def set_alarm():
#     print("Please specify the time for the alarm in the format of 'hour:minute AM/PM'")
#     while True:
#         alarm_time = input("Enter the time for the alarm: ")
#         if alarm_time:
#             try:
#                 alarm_time = datetime.strptime(alarm_time, '%I:%M %p')
#                 current_time = datetime.now().strftime('%I:%M %p')
#                 while datetime.now().strftime('%I:%M %p') != alarm_time.strftime('%I:%M %p'):
#                     # Wait until the alarm time is reached
#                     pass
#                 print("Alarm!")
#                 speak("Alarm!")
#                 break
#             except ValueError:
#                 print("Sorry, I couldn't understand the time. Please try again.")
#         else:
#             print("Please specify the time for the alarm.")
# set_alarm()
        
# def Reply(question, chat_log=None):
#     if chat_log is None:
#         chat_log = chat_log_template
#     prompt = f'{chat_log}You : {question}\nJarvis :'
#     response = completion.create(
#         prompt=prompt, engine="davinci", stop=['\nYou'], temperature=0.9,
#         top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
#         max_tokens=150)
#     answer = response.choices[0].text.strip()
#     return answer

#PLay music
# Function to record and recognize voice command
def recognize_voice():
    with sr.Microphone() as source:
        print("Listening...")
        audio = sr.Recognizer().listen(source)
        try:
            # Use Google Speech Recognition to recognize the voice command
            command = sr.Recognizer().recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("Sorry, I'm having trouble recognizing your voice.")
    return None

# Function to play music
def play_music():
    print("Playing music...")
    music_dir = "D:\Songs"  # Replace with the path to your music folder
    songs = os.listdir(music_dir)
    print("Songs in the folder:")
    for i, song in enumerate(songs):
        print(f"{i+1}. {song}")
    while True:
        print("Please enter the song number you want to play (or 'exit' to cancel):")
        choice = recognize_voice()
        if choice:
            if choice.isdigit():
                song_number = int(choice)
                if song_number >= 1 and song_number <= len(songs):
                    print(f"Playing: {songs[song_number-1]}")
                    os.startfile(os.path.join(music_dir, songs[song_number-1]))
                    break
                else:
                    print("Invalid song number. Please try again.")
            elif 'exit' in choice:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Please enter a valid song number or 'exit' to cancel.")
        command = parseCommand().lower()

             
          
# Main loop     
if __name__ == '__main__':
    wishMe()
    speak('how may I help you?')
 
    while True:
        query = parseCommand().lower().split()
 
        if query[0] == activationWord:
            query.pop(0)
 
            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else: 
                    query.pop(0) # Remove say
                    speech = ' '.join(query)
                    speak(speech)
 
            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('edge').open_new(query)
 
            
            # Wikipedia 
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Searching Wikipedia....')
                speak(search_wikipedia(query))
                
            
            # Wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')
                try: 
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('Unable to compute.')
 
            
            # Note taking
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('Note written')
 
             # Music Playing
            if query[0] == 'play music':
                speak('Playing music')
                music_dir = 'D:\\Music'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir,songs[0]))

            #time
            elif 'time' in query:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

            #news
            elif 'news' in query:
                news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/india")
                speak(f'Here are some headlines from the Times of India')

            # #openAIClient
            # if query[0] == 'chat':
            #     query = ' '.join(query[1:])
            #     speak(Reply(query))

            #Music Playing
        if 'play music' in query:
            play_music()
        else:
            print("Command not recognized")


            # if query == 'set alarm':
            #     query = ' '.join(query[1:]).lower().split()
            #     set_alarm()
            
            if query[0] == 'exit':
                speak('Goodbye')
                break
  



            
            

            
