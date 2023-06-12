import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
import pyaudio
import sys
from datetime import datetime
from datetime import date
import datetime
import time
import webbrowser
import wikipediaapi

# Create an instance of WikipediaAPI
wiki_wiki = wikipediaapi.Wikipedia('en')

recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

todo_list = ['go home', 'go dorm', 'record video']



def create_note():
    global recognizer

    speaker.say("what should i write on your note?")
    speaker.runAndWait()
    creatingthenote()

def creatingthenote():

    global recognizer
    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audios = recognizer.listen(mic)

                note = recognizer.recognize_google(audios)
                note = note.lower()
                print(note)

                speaker.say("choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audios = recognizer.listen(mic)

                filename = recognizer.recognize_google(audios)
                filename = filename.lower()
                print(filename)

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"successfully opened file with the name {filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("come again?")
            speaker.runAndWait()


def to_do():
    global recognizer

    speaker.say("what would you like to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio2 = recognizer.listen(mic)

                item = recognizer.recognize_google(audio2)
                item = item.lower()

                print(item)

                todo_list.append(item)
                done = True

                speaker.say(f"{item} added to your list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("come again please")
            speaker.runAndWait()


def show_to_do():
    speaker.say("the list is as follows")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("hello to you too what can i help you with")
    speaker.runAndWait()

def tell_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    speaker.say(f"the time is now {current_time}")
    speaker.runAndWait()
    print(current_time)

def tell_date():
    current_date = date.today().strftime("%Y-%m-%d")
    speaker.say(f"today is {current_date}")
    speaker.runAndWait()
    print(current_date)

def intro():
    speaker.say("my name is sophi, I am an AI programed to assist you in your day to day life by my developers mahiber gfuan")
    speaker.runAndWait()

def browse():
    speaker.say("what topic would you like search for")
    speaker.runAndWait()
    global recognizer
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                topic = recognizer.recognize_google(audio)
                speaker.say(topic)

                url='https://google.com/search?q='+topic
                webbrowser.get().open(url)



        except speech_recognition.UnknownValueError:
            print("say it again please")
            recognizer = speech_recognition.Recognizer()


def wikip():
    speaker.say("what topic would you like to ask me")
    speaker.runAndWait()
    searchw()


def searchw():
    global recognizer
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                topic = recognizer.recognize_google(audio)
                speaker.say(topic)

                search_results = wiki_wiki.page(topic)

                if search_results.exists():
                    speaker.say(search_results.summary[0:300])
                else:
                    speaker.say("Sorry but i don't know about that.")
                done = True

        except speech_recognition.UnknownValueError:
            print("say it again please")
            recognizer = speech_recognition.Recognizer()


def exitt():
    speaker.say("goodbye?")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": to_do,
    "show_todo": show_to_do,
    "time": tell_time,
    "date": tell_date,
    "introduction":intro,
    "wiki": wikip,
    "goodbye": exitt
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()


assistant.save_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()
            print(message)
        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
