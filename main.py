import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
import sys


recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150 )

todo_list=['go home','go church','record video']




assistant =GenericAssistant('intents.json')
assistant.train_model()

assistant.request("how are you")
