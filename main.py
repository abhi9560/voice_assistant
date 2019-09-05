from tkinter import *
from tkinter import ttk

import pyttsx3
import engineio

import speech_recognition as sr

from threading import *

import datetime

import wikipedia

import winsound

import webbrowser

import os

from bs4 import BeautifulSoup
import requests,json
import time

global root
engine = pyttsx3.init()
# en_voice_id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
# engine.setProperty('voice', en_voice_id)
r = sr.Recognizer()
r.pause_threshold = 0.7
r.energy_threshold = 400
chrome_path = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

def speak(audio_text):
    engine.say(audio_text)
    engine.runAndWait()

def weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
    complete_url = base_url + city
    response = requests.get(complete_url)
    time.sleep(0.5)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
    z = x["weather"]
    weather_description = z[0]["description"]
    speak("It is" + weather_description)

def temperature(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
    complete_url = base_url + city
    response = requests.get(complete_url)
    time.sleep(0.5)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
    current_temperature = y["temp"]
    speak("The current temperature in " + city + "is" + str(current_temperature-273.15))

def humidity(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
    complete_url = base_url + city
    response = requests.get(complete_url)
    time.sleep(0.5)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
    current_humidiy = y["humidity"]
    speak("The current humidity is " + str(current_humidiy))

class voice_input(Thread):
    def run(self):
        speak("Good Morning! How are you")
        with sr.Microphone() as source:
            speak("Listening")
            audio = r.record(source, duration = 5)
        message = str(r.recognize_google(audio))
        speak("You said" + message)

def take_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak('Say something after the beep')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        winsound.Beep(1000,500)
        audio = r.record(source, duration = 5)
    try:
        query = r.recognize_google(audio, language='en-in')
        speak(query)
    except Exception as e:
       speak("Say that again please")  
       return None
    return query

def google(text):
    webbrowser.get(chrome_path).open('https://www.google.com/search?ei=ReVkXb2SAsvfz7sPlLmSqAU&q='+text+'&oq='+text+'&gs_l=psy-ab.3..0l2j0i131j0j0i10j0l3j0i10j0.7890.8170..8454...0.3..0.192.505.0j3......0....1..gws-wiz.......0i71j0i67.pry4s89OA-4&ved=0ahUKEwj9yILbzKLkAhXL73MBHZScBFUQ4dUDCAo&uact=5')

def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am you Personal Assistant at your service. Please Click on Mic button to say something")    

def wiki(text):
    speak(wikipedia.summary(text , sentences = 2))

def text_processing(text):
    stopwords = ["what","is","according","weather","hey","hi","to","wikipedia","search","please",
    "play","today","today's","which","day's","as","per","the","in","temperature","humidity"]
    for i in stopwords:
        text = text.replace(i,'')
    return text.strip()

def youtube(texter):
	response = requests.get('https://www.youtube.com/results?search_query='+texter)
	soup = BeautifulSoup(response.text,'lxml')
	link = soup.find_all('a')[44]
	links = 'https://www.youtube.com'+link.get('href')
	webbrowser.get(chrome_path).open(links)

def calendar(temp):
    dic = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thurday',4:'Friday',5:'Saturday',6:'Sunday'}
    speak("Today is "+ dic[temp])

def adding_note():
    speak("Please say what to add")
    result = take_voice_input()
    with open('notes.txt','a+') as f:
        f.write(result)
    speak("Notes added successfully")

def reading_note():
    try:
        f = open('notes.txt','r')
        texter = f.read()
        if texter:
        	print(texter)
        	speak(texter)
        else:
            speak("No text in file")
    except FileNotFoundError:
        speak("No notes found")

def deleting_note():
    f = open('notes.txt','w').close()
    speak("All notes cleared")

def content_opener(result):
    result = text_processing(result).strip()
    print(result)
    if result == 'open explorer':
        os.system('explorer')
    if result == 'open c drive':
        os.startfile(r"C:")
    if result == 'open e drive':
        os.startfile(r"E:")
    if result == 'open f drive':
        os.startfile(r"F:")
    if result == 'open d drive':
        os.startfile(r"D:")
    if result == 'open g drive':
        os.startfile(r"G:")
    if 'add' in result and 'note' in result or 'end' in result:
        adding_note()
    if 'notes' in result and 'read' in result or 'red' in result or 'open' in result:
        print("GOOD")
        reading_note()
    if 'delete' in result and 'notes' in result:
        deleting_note()
    if 'date' in result:
        strdate = datetime.datetime.now().strftime("%d %m %Y")
        speak(f"Today's date is {strdate}")
    if 'day' in result:
        temp = datetime.datetime.today().weekday()
        calendar(temp)
    if 'year' in result or 'yer' in result:
        speak("This is" + str(datetime.datetime.now().year))
    if 'time' in result:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"The time is {strTime}")

def handle_click(event):
    result = take_voice_input()
    if result:
        result = result.lower()
        if 'exit' in result:
            root.destroy()
        if 'wikipedia' in result:
            speak('Searching Wikipedia...')
            result = text_processing(result)
            speak("According to Wikipedia")
            wiki(result)
        elif 'google' in result:
            result = text_processing(result)
            google(result)
        elif 'youtube' in result:
            result = text_processing(result)
            youtube(result)
        elif 'weather' in result:
            result = text_processing(result)
            weather(result)
        elif 'temperature' in result:
            result = text_processing(result)
            temperature(result)
        elif 'humidity' in result:
            result = text_processing(result)
            humidity(result)
        elif 'what is' in result and 'time' not in result:
        	result = text_processing(result)
        	google(result)
        else:
            content_opener(result)

def main():
    root = Tk()
    entry = Entry(root)
    root.title('Universal Search Bar')
    style = ttk.Style()
    style.theme_use('winnative')
    photo = PhotoImage(file='microphone.png').subsample(6,6)
    obj1 = voice_input()
    voice_bt = Button(root, image=photo, bd=0,
        activebackground='#c1bfbf', overrelief='groove', relief='sunken') 
    voice_bt.bind("<1>", handle_click)
    voice_bt.grid(row=4, column=5)
    greetings()
    root.mainloop()

main()
