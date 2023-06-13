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
import pywhatkit
import tkinter as tk
from tkinter import scrolledtext
import threading

# Create an instance of WikipediaAPI
wiki_wiki = wikipediaapi.Wikipedia('en')

recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

todo_list = ['go home', 'go dorm', 'record video']


def update_gui(user_command, program_reply):
    text_widget.insert(tk.END, f"You: {user_command}\n")
    text_widget.insert(tk.END, f"Sophi: {program_reply}\n")
    text_widget.see(tk.END)

def hear():
    global recognizer
    global user
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                update_gui("", "listening")
                word = recognizer.recognize_google(audio)
                update_gui(word, "")
                return word

        except speech_recognition.UnknownValueError:
            say(f"I am sorry{user}!I don't understand")
            recognizer = speech_recognition.Recognizer()

def say(key):
    speaker.say(key)
    speaker.runAndWait()
    update_gui("", key)

def create_gui():
    global text_widget
    root = tk.Tk()
    root.title("Voice Interaction GUI")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

def create_note():
    global recognizer

    say("what should i write on your note?")
    note = hear()
    say("choose a filename")
    filename = hear()
    with open(filename, 'w') as f:
        f.write(note)
        say(f"successfully opened file with the name {filename}")

def to_do():
    global recognizer

    say("what would you like to add?")

    item=hear()
    todo_list.append(item)

    say(f"{item} added to your list!")

def show_to_do():
    say("the list is as follows")
    for item in todo_list:
        say(item)
def hello():
    global user
    say(f"hello to you too {user}, what can i help you with?")

def tell_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    say(f"the time is now {current_time}")
    print(current_time)

def tell_date():
    current_date = date.today().strftime("%Y-%m-%d")
    say(f"today is {current_date}")
    print(current_date)

def intro():
    say("my name is Sophi, I am an AI programed to assist you in your day to day life by my developers Group 9")

def browse():
    say(f"what topic would would you like search for{user}")

    topic = hear()

    url = 'https://google.com/search?q='+topic
    webbrowser.get().open(url)

    say(f"here is what I found {user}")

def locate():
    say("what place should i locate")

    place = hear()

    url = 'https://google.nl/maps/place/' + place +'/&amp;'
    webbrowser.get().open(url)

    say(f"here is the {place} I found , {user}")

def plyyt():
    say("what video do want to play")

    word = hear()

    pywhatkit.playonyt(word)
def wikip():
    say("what topic would you like to ask me")

    topic = hear()
    search_results = wiki_wiki.page(topic)

    if search_results.exists():
        say(search_results.summary[0:300])
    else:
        speaker.say(f"Sorry but i don't know about about{topic}.")


def exitt():
    say("goodbye?")
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": to_do,
    "show_todo": show_to_do,
    "time": tell_time,
    "date": tell_date,
    "introduction":intro,
    "browse":browse,
    "locate":locate,
    "ytply":plyyt,
    "wiki": wikip,
    "goodbye": exitt
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

assistant.save_model()
assistant.load_model()

say("for better experience can you please share your name")
user = hear()
say(f"thank you {user}")
intro()
def main():
    gui_thread = threading.Thread(target=create_gui)
    gui_thread.start()

    assistant.load_model()

    while True:
        message = hear()
        message = message.lower()
        print(message)
        assistant.request(message)

if __name__ == "__main__":
    main()

