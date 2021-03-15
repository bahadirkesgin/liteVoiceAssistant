# -*- coding: utf-8 -*-
import SpeechRecognition as sr
import random
from datetime import datetime
from playsound import playsound
from gtts import gTTS
import wikipedia
import random
import os
import time
from selenium import webdriver
from nltk.tokenize import sent_tokenize
import spotify

re = sr.Recogniser()
mic = sr.Microphone()

def speak(text, num):
    tts = gTTS(text, lang ='tr')
    file = "audio-"+str(num)+".mp3"
    print(text)
    tts.save(file)
    playsound(file)

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
            
        if "dur" in str(text) or "çıkış" in str(text) or "görüşürüz" in str(text):
            break
            
        if 'wikipedia' in text:
            text = text.replace("wikipedia", "")
            wikipedia_search(text)
                  
        elif 'saat kaç' in text:
            break
        
        elif 'ara' in text:
            text = text.replace("ara", "")
            google_search(text)
            speak("İşte bunları buldum", 6)
            
        elif "hesapla" or "kaç eder" or "kaçtır" in text: 
            break    
            
        elif 'google aç' in text:
            driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            driver.get("https://google.com")
            
        elif 'youtube aç' in text: 
            text = text.replace("youtube", "")
            youtube_search(text)
             
        elif 'müzik çal' in text:
            break
        elif 'hava' in text:
            break
        elif 'sesi aç' or 'sesi yükselt' or 'sesi arttır' in text:
            break
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
    search_result = wikipedia.search(stext)
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