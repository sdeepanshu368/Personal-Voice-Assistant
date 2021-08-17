from bs4 import BeautifulSoup
import cv2
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import instaloader
import numpy as np
import operator
import os
import os.path
import psutil
import pyautogui
import pyjokes
import PyPDF2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import pyttsx3
from pywikihow import search_wikihow
import pywhatkit as kit
import random
import requests
from requests import get
from requests_html import HTMLSession
import smtplib
import speech_recognition as sr
import speedtest
import subprocess
import sys
import time
from twilio.rest import Client
import urllib.request
import webbrowser
import wikipedia
from jarvis import Ui_MainWindow
from features import MyAlarm


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
# engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    # if hour >= 0 and hour < 12:
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Personal Voice Assistant Sir. Please tell me how may I help you")


def sendEmail(self):
    speak("Do you want to send the email with an attachment")
    choice = self.takeCommand()
    if 'yes' in choice:
        your_email = "youremail@gmail.com"
        your_email_password = "password"
        send_to = "receiverid@gmail.com"
        speak('Okay Sir, What is the Subject')
        subject = self.takeCommand()
        speak('And What is the Message Sir')
        mail_message = self.takeCommand()
        speak('Please enter the path of file you want to attach')
        file_location = input('Please enter the path of file here: ')
        speak('Please wait, I am sending the email')
        try:
            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = send_to
            msg['Subject'] = subject

            msg.attach(MIMEText(mail_message, 'plain'))

            # Setup the attachment
            filename = os.path.basename(file_location)
            attachment = open(file_location, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # Attach the attachment to the MIMEMultipart object
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(your_email, your_email_password)
            text = msg.as_string()
            server.sendmail(your_email, send_to, text)
            server.quit()
            speak('Email has been sent successfully')
        except Exception as e:
            print(e)
            speak('Something went wrong. I am unable to send the email.')
    else:
        your_email = "youremail@gmail.com"
        your_email_password = "password"
        send_to = "receiverid@gmail.com"
        speak('Okay Sir, What is the Message')
        mail_message = self.takeCommand()
        speak('Please wait, I am sending the email')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(your_email, your_email_password)
            server.sendmail(your_email, send_to, mail_message)
            server.quit()
            speak('Email has been sent successfully')
        except Exception as e:
            print(e)
            speak('Something went wrong. I am unable to send the email.')


def news():
    try:
        news_url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=4388615525204ff7ac5de48d7502f6e3'
        main_page = requests.get(news_url).json()
        # print(main_page)
        articles = main_page['articles']
        # print(articles)
        head = []
        total_news = 10
        for ar in articles:
            head.append(ar["title"])
        for i in range(total_news):
            if i == 0:
                speak(f"Today's first news is. {head[i]}")
            elif i == total_news-1:
                speak(f"Today's last news is. {head[i]}")
            else:
                speak(f"Moving to our next news. {head[i]}")
    except:
        speak('Sorry Sir, I a unable to process this request')


def pdf_reader():
    try:
        speak('Please enter path of pdf file')
        ppath = input('Please enter path of pdf file here: ')
        book = open(ppath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(book)
        pages = pdfReader.numPages
        speak(f'This book is of {pages} pages')
        speak('Sir please enter the page number I have to read')
        pg = int(input("Please enter the page number here: "))
        page = pdfReader.getPage(pg)
        text = page.extractText()
        speak(text)
    except:
        speak('Sorry Sir, I a unable to process this request')


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        # speak('Please say wake up to continue')
        # while True:
        #     self.command = self.takeCommand()
        #     if "wake up" in self.command:
        #         self.TaskExecution()
        #     elif "goodbye" in command:
        #         sys.exit()
        self.TaskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            # audio = r.listen(source, timeout=1, phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            # print(e)
            speak("Say that again please")
            return "None"
        query = query.lower()
        return query

    def TaskExecution(self):
        chrome_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        wishMe()
        while True:
            self.query = self.takeCommand()

            if 'time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'battery' in self.query:
                try:
                    battery = psutil.sensors_battery()
                    percentage = battery.percent
                    speak(f'Sir the system has {percentage} percent battery')
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'volume up' in self.query:
                pyautogui.press('volumeup')

            elif 'volume down' in self.query:
                pyautogui.press('volumedown')

            elif 'volume mute' in self.query:
                pyautogui.press('volumemute')

            elif 'open notepad' in self.query:
                codePath = r"C:\Windows\System32\notepad.exe"
                os.startfile(codePath)

            elif 'close notepad' in self.query:
                speak('Okay Sir, Closing notepad')
                os.system('taskkill /f /im notepad.exe')

            elif 'open vs code' in self.query:
                codePath = r"C:\Users\Intel\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                os.startfile(codePath)

            elif 'command prompt' in self.query or 'cmd' in self.query:
                os.system('start cmd')

            elif 'music' in self.query or 'song' in self.query:
                try:
                    music_dir = r"C:\Users\Intel\PycharmProjects\JARVIS"
                    songs = os.listdir(music_dir)
                    # print(songs)
                    # rd = random.choice(songs)
                    for song in songs:
                        if song.endswith('.mp3'):
                            os.startfile(os.path.join(music_dir, song))
                            speak('Playing music for you')
                except:
                    speak('Sorry Sir I am unable to play a song')

            elif 'screenshot' in self.query:
                speak('Sir what should I name this file')
                fname = self.takeCommand()
                speak('Please hold on for few seconds, I am taking the screenshot')
                time.sleep(2)
                img = pyautogui.screenshot()
                img.save(f"{fname}.png")
                speak('Done Sir, the screenshot is saved in the main folder')

            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif 'change folder visibility' in self.query:
                speak('Sir please tell me, you want to hide this folder or make it visible')
                condition = self.takeCommand()
                if 'hide' in condition:
                    os.system('attrib +h /s /d')
                    speak('Sir all files in this folder are now hidden')
                elif 'visible' in condition:
                    os.system('attrib -h /s /d')
                    speak('Sir all files in this folder are now visible')

            elif 'do some calculation' in self.query or 'calculate' in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak('What do you want to calculate Sir')
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)
                try:
                    def get_op(op):
                        return {
                            '+': operator.add,
                            '-': operator.sub,
                            '*': operator.mul,
                            'divide': operator.__truediv__,
                        }[op]

                    def eval_expr(op1, oper, op2):
                        op1, op2 = int(op1), int(op2)
                        return get_op(oper)(op1, op2)

                    speak('Result is')
                    speak(eval_expr(*(my_string.split())))
                except:
                    speak('Sorry Sir, I am unable to calculate. Please enter valid input')

            elif 'alarm' in self.query:
                speak('Sir please tell the time to set an alarm, for example you can say. 6:25 AM')
                alarm_time = self.takeCommand()
                alarm_time = alarm_time.replace('.', '')
                alarm_time = alarm_time.upper()
                try:
                    MyAlarm.alarm(alarm_time)
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP Address is {ip}")

            elif 'where i am' in self.query or 'where we are' in self.query or 'location' in self.query:
                speak('Wait Sir, let me check')
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                    geo_request = requests.get(url)
                    geo_data = geo_request.json()
                    print(geo_data)
                    city = geo_data['city']
                    state = geo_data['region']
                    country = geo_data['country']
                    longitude = geo_data['longitude']
                    latitude = geo_data['latitude']
                    timezone = geo_data['timezone']
                    speak(f'Sir I am not sure but I think we are in {city} city of {state} of country {country}')
                    speak(f'longitude is {longitude} and latitude is {latitude} and timezone is {timezone}')
                except Exception as e:
                    speak('Sorry sir due to some issues I am not able to find our location')

            elif 'internet speed' in self.query:
                # try:
                #     os.system('cmd /k "speedtest"')
                # except:
                #     speak('Can not connect to the internet')
                speak('Wait Sir let me check')
                st = speedtest.Speedtest()
                dl = st.download()/8000000
                ul = st.upload()/8000000
                speak(f'Sir, the download speed is {round(dl, 2)} maga bytes per second and the upload speed is {round(ul, 2)} maga bytes per second')

            elif 'weather' in self.query or 'temperature' in self.query:
                session = HTMLSession()
                speak('Please tell me the city name Sir. For example you can say Mumbai')
                query = self.takeCommand()
                try:
                    url = f"https://www.google.com/search?q={query}+weather"
                    res = session.get(url)
                    data = BeautifulSoup(res.content, "html.parser")
                    location = data.find("div", class_="wob_loc mfMhoc")
                    date = data.find("div", class_="wob_dts")
                    weather = data.find("span", {"id": "wob_dc"})
                    temperature = data.find("span", class_="wob_t TVtOme")
                    speak(f"It's {date.text} and weather of {location.text} is {weather.text} and the temperature is {temperature.text} degree celsius")
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'wikipedia' in self.query:
                try:
                    speak('Searching Wikipedia...')
                    nquery = self.query.replace("wikipedia", "")
                    results = wikipedia.summary(nquery, sentences=2, auto_suggest=False)
                    speak("According to Wikipedia")
                    speak(results)
                except:
                    speak('Sorry Sir, I am unable to find the information')

            elif 'stackoverflow' in self.query:
                webbrowser.get(chrome_path).open("www.stackoverflow.com")

            elif 'facebook' in self.query:
                webbrowser.get(chrome_path).open("www.facebook.com")

            elif 'open youtube' in self.query:
                webbrowser.get(chrome_path).open("www.youtube.com")

            elif 'play a song on youtube' in self.query or 'play a video on youtube' in self.query:
                try:
                    speak('What song do you want to play Sir')
                    song_name = self.takeCommand()
                    kit.playonyt(song_name)
                    speak(f'Playing {song_name}')
                except:
                    speak('Sorry Sir, I am unable to find the video')

            elif 'open google' in self.query:
                webbrowser.get(chrome_path).open("www.google.com")

            elif 'search on google' in self.query or 'google' in self.query or 'search' in self.query:
                try:
                    speak('Sir, what do you want to search on Google')
                    cm = self.takeCommand()
                    webbrowser.open(f"{cm}")
                    speak('Wait Sir I am searching')
                except:
                    speak('Sorry Sir, I am unable to search')

            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'pdf' in self.query:
                pdf_reader()

            elif 'news' in self.query:
                news()

            elif 'whatsapp' in self.query:
                try:
                    speak('What should I say')
                    msg = self.takeCommand()
                    kit.sendwhatmsg("+91 9999999999", msg, 11, 10)
                    speak('message has been sent')
                except:
                    speak('Sorry Sir, I am unable to send whatsapp message')

            elif 'email' in self.query:
                sendEmail(self)

            elif 'instagram' in self.query:
                try:
                    speak('Sir please enter user name')
                    uname = input("Enter username here: ")
                    webbrowser.open(f"www.instagram.com/{uname}")
                    speak(f"Sir here is the instagram profile of {uname}")
                    time.sleep(5)
                    speak(f'Sir would you like to download the profile picture of {uname}')
                    condition = self.takeCommand()
                    if 'yes' in condition:
                        mod = instaloader.Instaloader()
                        mod.download_profile(uname, profile_pic_only=True)
                        speak('Done Sir, profile picture is saved in our main folder')
                    else:
                        pass
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'tweet' in self.query or 'twitter' in self.query:
                try:
                    speak('What do you want to tweet Sir')
                    tweet = self.takeCommand()
                    speak('Wait Sir, I am tweeting')
                    os.system(f'python bot\\TwitterBot.py "{tweet}"')
                except:
                    speak('Sorry Sir, I am unable to tweet')

            elif 'activate how to do' in self.query:
                speak('How to do mode is activated Sir please tell me what you want to know')
                how = self.takeCommand()
                try:
                    if 'exit' in how:
                        speak('Okay Sir, How to do mode deactivated')
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak('Sorry Sir, I am not able to find this')

            elif 'open webcam' in self.query or 'open camera' in self.query:
                try:
                    speak('Opening webcam, you can press escape key to quit')
                    cap = cv2.VideoCapture(0)
                    while True:
                        ret, img = cap.read()
                        cv2.imshow('webcam', img)
                        k = cv2.waitKey(50)
                        if k == 27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'open mobile camera' in self.query:
                try:
                    URL = 'http://192.168.43.1:8080/shot.jpg'
                    while True:
                        img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
                        img = cv2.imdecode(img_arr, -1)
                        cv2.imshow('IPWebcam', img)
                        q = cv2.waitKey(1)
                        if q == 27:
                            break
                    cv2.destroyAllWindows()
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'send message' in self.query or 'sms' in self.query:
                try:
                    speak('Sir, what should I say')
                    sms = self.takeCommand()
                    account_sid = 'TWILIO_ACCOUNT_SID'
                    auth_token = 'TWILIO_AUTH_TOKEN'
                    client = Client(account_sid, auth_token)
                    message = client.messages \
                        .create(
                            body=sms,
                            from_='+15017122661',
                            to='+15558675310'
                        )
                    print(message.sid)
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'call' in self.query:
                try:
                    account_sid = 'TWILIO_ACCOUNT_SID'
                    auth_token = 'TWILIO_AUTH_TOKEN'
                    client = Client(account_sid, auth_token)
                    message = client.calls \
                        .create(
                            twiml='<Response><Say>Calling...</Say></Response>',
                            from_='+15017122661',
                            to='+15558675310'
                        )
                    print(message.sid)
                except:
                    speak('Sorry Sir, I am unable to process this request')

            elif 'shutdown the system' in self.query:
                os.system('shutdown /s /t S')

            elif 'restart the system' in self.query:
                os.system('shutdown /r /t S')

            elif 'sleep the system' in self.query:
                # powercfg - hibernate off
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

            elif 'you can sleep' in self.query:
                speak("Okay Sir, I am going to sleep you can call me anytime.")
                sys.exit()
                # break


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection

    def startTask(self):
        self.ui.movie = QtGui.QMovie('images\\Jarvis.gif')
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie('images\\initiating.gif')
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
