# -*- coding: utf-8 -*-
import SpeechRecognition as sr
from datetime import datetime
from playsound import playsound
from gtts import gTTS
import wikipedia
import random
import os
import time
import wolframalpha
import requests
from selenium import webdriver
from nltk.tokenize import sent_tokenize

re = sr.Recogniser()
mic = sr.Microphone()

def speak(text, num = random.randint(50,3000)):
    tts = gTTS(text, lang ='tr')
    file = "audio-"+str(num)+".mp3"
    print(text)
    tts.save(file)
    playsound(file)
    os.remove(file)

def listen():
    u_text = ""
    with mic as source:
        voice = re.listen(source)
        try:
            u_text = re.recognize_google(voice)
            print(voice + "dediniz")
        except sr.UnkownValueError:
            excep_response = "Üzgünüm, ne dediğinizi anlamadım. Lütfen tekrar konuşun"
            speak(excep_response, 1)
    return u_text
        
# TODO: add specific sentences to react
    if __name__=='__main__':
        username = ''
        speak("Merhaba"+ username + "ben kişisel asistanınız rigel", 5)
    if username == '':
        speak("Size nasıl hitap etmemi istersiniz", 4)
        username = listen().lower()
        
    while(1):
        speak("Size nasıl yardımcı olabilirim", 3)
        text = listen().lower()
        
        if text==0:
            continue
        
        if "çıkış" in text or "görüşürüz" in text:
            print("Görüşmek üzere!")
            speak("Görüşmek üzere")
            break
        
        elif "tarih" in text:
            date = datetime.date.today()
            date = date.strftime("%d/%m/%y")
            speak(f"Bugünün tarihi {date}")
            print(f"Bugünün tarihi:{date}")
        
        elif 'wikipedia' in text:
            text = text.replace("wikipedia", "")
            wikipedia_search(text)
                  
        elif 'saat kaç' in text:
            cur_time = datetime.datetime.now()
            cur_time = cur_time.strftime("%H:%M:%S")
            speak(f"Saat {cur_time}")
        
        elif 'ara' in text:
            text = text.replace("ara", "")
            google_search(text)
            speak("İşte bunları buldum", 6)
            
        elif "hesapla" in text:
            api_id = "LYH8JE-XHUWTAJVJX"
            wolfram_cli = wolframalpha.Client(api_id)
            indx = text.split().index('hesapla')
            text = text.split()[indx + 1:]
            res = wolfram_cli.query(' '.join(text))
            answer = next(res.results).text
            print("İşlemin sonucu: " + answer)
            speak("İşlemin sonucu " + answer)
            
            
        elif 'google aç' in text:
            driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            driver.get("https://google.com")
            
        elif 'youtube aç' in text: 
            text = text.replace("youtube", "")
            youtube_search(text)
             
        
        elif 'müzik çal' in text:
            text = text.replace("youtube", "")
            youtube_search(text)
            
        
        elif 'hava durumu' in text:
            text_city = text.replace("hava durumu", "")
            api_key="e2024c81d0ce1686c5b70152fdd01b9d"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            full_url = base_url + "appid="+api_key+"&q="+ text_city +"&lang=tr"+"&units=metric"
            response = requests.get(full_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                cur_temp = y["temp"]
                cur_hum = y["humidity"]
                z = x["weather"]
                weather_des = z[0]["description"]
                w_f1 = f"Bugün {text_city} ilinde hava {weather_des} "
                w_f2 = f"{cur_temp} derece "
                w_f3 = f"ve nem oranı {cur_hum}"
                weather_forecast = w_f1 + w_f2 + w_f3
                speak(weather_forecast)
                print(weather_forecast)
        
        elif "haberler" in text:
            driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            driver.get("https://www.bbc.com/turkce")
            speak("BBC Türkçeden haberler, iyi okumalar")
            time.sleep(6)
        
        else:
           speak("Üzgünüm, isteğinizi yerine getiremiyorum", 2)

    
def google_search(stext):
    stext = stext.split()
    search_object = ""
    for i in stext[1:-2]:
        search_object = search_object + i
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    driver.get("http://google.com/search?q=" + search_object)
    
def wikipedia_search(stext): # stext = searched text
    wikipedia.set_lang("tr")
    search_result = wikipedia.summary(stext, sentences=3)
    random_num =  random(50,1000)
    sptext = search_result.sent_tokenize(search_result)
    speak(sptext, random_num)
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    driver.get("https://tr.wikipedia.org/wiki/" + stext)
    
def youtube_search(stext):
    stext = stext.split()
    song_name = ""
    for i in stext[1:-1]:
        song_name = song_name + i
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    driver.get("https://www.youtube.com/results?search_query=" + song_name);
    select_element = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for option in select_element:
        option.find_element_by_xpath('//*[@id="video-title"]').click()
        break
    return driver
