# Ref: https://github.com/NijatZeynalov/Scraper-Chatbot?tab=readme-ov-file 
#
# REMEMBER to pip install everything below from the terminal
# pip install pyttsx3 SpeechRecognition datetime wikipedia requests bs4 google-api-python-client oauth2client httplib2 googletrans

import pyttsx3
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import random
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from googletrans import Translator
import threading

b = "Spartan: "
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Predefined lists for Spartan's responses
motiv = "Sometimes later becomes never. Do it now. EE104, I believe in you, you have made me."
need_list = ['EE104, what can I do for you?', 'Do you want something else?', ...]
sorry_list = ['EE104, I am sorry I don\'t know the answer', 'I don\'t have an idea about it, EE104', ...]
bye_list = ['Goodbye, EE104. I will miss you', 'See you EE104', 'Bye, don\'t forget I will always be here']
comic_list = ['It is not a joke, EE104. I was serious', 'Do you think that it is a joke? Be nice!']
greet_list = ['Hi EE104', 'Hi my dear']

# Initialize Translator for language translation feature
translator = Translator()

# Text-to-Speech Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greeting Function Based on Time of Day
def greetings():
    h = int(datetime.datetime.now().hour)
    if h > 8 and h < 12:
        print(b, 'Good Morning. My name is Spartan. Version 1.00')
        speak('Good morning. My name is Spartan. Version 1.00')
    elif h >= 12 and h < 17:
        print(b, "Good afternoon. My name is Spartan. Version 1.00")
        speak('Good afternoon. My name is Spartan. Version 1.00')
    else:
        print(b, 'Good evening! My name is Spartan. Version 1.00')
        speak('Good evening. My name is Spartan. Version 1.00')
    print(b, 'How can I help you, EE104?')
    speak('How can I help you, EE104?')

# Weather Function
def weather_Spartan(city):
    try:
        url = "https://www.google.com/search?q=" + "weather " + city
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        data = str.split('\n')
        time = data[0]
        sky = data[1]
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        pos = strd.find('Wind')
        other_data = strd[pos:]

        print("At ", city)
        print("Temperature is", temp)
        print("Time: ", time)
        print("Sky Description: ", sky)
        print(other_data)
    except:
        sorry = random.choice(sorry_list)
        print(b, sorry)
        speak(sorry)

# Additional Function: Language Translation
def translate_text(text, dest_language):
    try:
        translation = translator.translate(text, dest=dest_language)
        print(b, "Translation:", translation.text)
        speak("Translation: " + translation.text)
    except Exception as e:
        print(b, "Sorry, I couldn't translate the text.")
        speak("Sorry, I couldn't translate the text.")

# Additional Function: Basic Math Calculations
def calculate(expression):
    try:
        result = eval(expression)
        print(b, "The result is:", result)
        speak("The result is: " + str(result))
    except:
        print(b, "Sorry, I couldn't calculate that.")
        speak("Sorry, I couldn't calculate that.")

# New function for setting reminders
def set_reminder():
    print(b, "What do you want me to remind you about?")
    reminder = input("EE104: ")
    print(b, "In how many seconds should I remind you?")
    try:
        timer = int(input("EE104: "))  # Taking input in seconds
        print(b, f"Reminder set for {timer} seconds.")
        time.sleep(timer)  # Wait for the specified time
        print(b, f"Reminder: {reminder}")  # Remind the user
        speak(f"Reminder: {reminder}")  # Voice reminder
    except ValueError:
        print(b, "Please enter a valid number for the timer.")
        speak("Please enter a valid number for the timer.")

# Main Command Function
def takeCommand():
    while True:
        print(" ")
        query = input("EE104: ")

        if 'who is' in query.lower():
            query = query.replace("who is", "")
            result = wikipedia.summary(query, sentences=2)
            print(b, result)
            speak(result)

        elif 'hello' == query:
            greet = random.choice(greet_list)
            print(b, greet)
            speak(greet)

        elif 'play' in query.lower():
            query = query.replace("play", "")
            webbrowser.open("https://www.youtube.com/results?search_query=" + query)
            speak('Opening YouTube to play ' + query)

        elif query == 'exit' or query == "bye":
            goodbye = random.choice(bye_list)
            print(b, goodbye)
            speak(goodbye)
            break

        elif 'motivate' in query:
            print(b, motiv)
            speak(motiv)

        elif 'facebook' in query:
            webbrowser.open("https://www.facebook.com")
            speak('Opening Facebook')

        elif 'weather' in query.lower():
            city = query.replace("weather", "").strip()
            weather_Spartan(city)

        elif 'shutdown laptop' in query.lower():
            speak("Shutting down the laptop")
            os.system("shutdown /s /t 1")
        
        elif 'translate' in query.lower():
            print("Enter the phrase you want to translate:")
            phrase = input("Phrase: ")
            print("Enter the destination language (e.g., 'es' for Spanish, 'fr' for French):")
            lang = input("Language Code: ")
            translate_text(phrase, lang)

        elif 'calculate' in query.lower():
            print("Enter the expression you want to calculate (e.g., '5 + 3'):")
            expression = input("Expression: ")
            calculate(expression)

        elif 'remind' in query.lower():
            set_reminder()

        elif 'what is' in query.lower():
            query = query.replace("what is", "")
            result = wikipedia.summary(query, sentences=2)
            print(b, result)
            speak(result)

        elif "when" or "how" or "is" or "are" in query:
            search = query
            url = 'https://search.yahoo.com/search?q=' + search
            webbrowser.open(url)

# Startup and Greeting
time.sleep(2)
print('Initializing...')
time.sleep(2)
print('Spartan is preparing...')
time.sleep(2)
print('Environment is building...')
time.sleep(2)
greetings()
takeCommand()
