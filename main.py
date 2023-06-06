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


assistant =GenericAssistant('intents.json')
assistant.train_model()

assistant.request("how are you")
