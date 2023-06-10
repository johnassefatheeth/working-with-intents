import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
import pyaudio
import sys
from datetime import datetime
from datetime import date
import datetime
import time

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

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audios = recognizer.listen(mic)

                note = recognizer.recognize_google(audios)
                note = note.lower()

                speaker.say("choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audios = recognizer.listen(mic)

                filename = recognizer.recognize_google(audios)
                filename = filename.lower()

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
    speaker.say("what can i help you with")
    speaker.runAndWait()

def tell_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    speaker.say(f"the time is now {current_time}")
    speaker.runAndWait()

def tell_date():
    current_date = date.today().strftime("%Y-%m-%d")
    speaker.say(f"today is {current_date}")
    speaker.runAndWait()

def sets_alarm():
    global recognizer
    speaker.say("what time do you like your alarm to be")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audios = recognizer.listen(mic)

                ttime = recognizer.recognize_google(audios)
                ttime = ttime.lower()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("say it again please?")
            speaker.runAndWait()

        sets_alarm(ttime)

    def set_alarm(alarm_time):
        speaker.say("what would you like to here when the alarm strikes")
        speaker.runAndWait()

        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audios = recognizer.listen(mic)

                    mesage = recognizer.recognize_google(audios)
                    mesage = mesage.lower()

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("come again please")
                speaker.runAndWait()
        while True:
            current_time = time.strftime('%I:%M:%S %p')  # Get the current time as a string in 12-hour format
            if current_time == alarm_time:
                speaker.say(mesage)
                break
            time.sleep(1)

    # Set the alarm time (in 12-hour format)
    alarm_time = "03:01:00 PM"

    # Call the set_alarm function with the desired alarm time
    set_alarm(alarm_time)

def exitt():
    speaker.say("goodbye?")
    speaker.runAndWait()
    #sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": to_do,
    "show_todo": show_to_do,
    "time": tell_time,
    "date": tell_date,
    "set_alarm":sets_alarm,
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

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
