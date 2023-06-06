import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
import sys


recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150 )

todo_list=['go home','go church','record video']

def create_note():
    global recognizer

    speaker.say("what should i write on your note?")
    speaker.runAndWait()

    done= False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note =recognizer.recognize_google(audio)
                note =note.lower()

                speaker.say("choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)

                filename= recognizer.recognize_google(audio)
                filename=filename.lower()

            with open(filename,'w') as f:
                f.write(note)
                done = True
                speaker.say(f"successfully opened file with the name {filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer= speech_recognition.Recognizer()
            speaker.say("come again?")
            speaker.runAndWait()


def to_do():
    global recognizer

    speaker.say("what would you like to add?")
    speaker.runAndWait()

    done=False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio= recognizer.listen(mic)

                item=    recognizer.recognize_google(audio)
                item=item.lower()

                todo_list.append(item)
                done=True

                speaker.say(f"{item} added to your list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer= speech_recognition.Recognizer()
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


def quit():
    speaker.say("goodbye sir")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note":create_note,
    "add_todo":to_do,
    "show_todo": show_to_do,
    "goodbye":quit
}



assistant =GenericAssistant('intents.json')
assistant.train_model()

assistant.request("how are you")
