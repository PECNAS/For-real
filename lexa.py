#! /usr/bin/env python
# -*-coding:utf-8-*-

# Голосовой ассистент ЛЕХА 1.0 БЕТА
import os
import sys
import time
import speech_recognition as sr
import datetime
import pyttsx3

from fuzzywuzzy import fuzz

opts = {
	"alias": ("лёха","лёх","лёша","алескей","ассистент","лёш"),
	"tbr": ("скажи", "пожалуйста", "выполни"),
	"cmds": {
		"ctime": ("сколько время", "который час"),
		"joke": ("шутка", "расскажи шутку"),
		"google": ("гугл", "открыть гугл", "открой гугл"),
		"stop": ("стоп", "спасибо за помощь", "заканчивай работу")
	}
}


  #функции
def speak(what):
	print( what )
	speak_engine.say( what )
	speak_engine.runAndWait()
	speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)                

        if voice.startswith(opts["alias"]):
            # обращаются к Джарвису
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])


    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] ОШИБКА, ОШИБКА НЕТ ПОДКЛЮЧЕНИЕ К ИНТЕРНЕТУ!!!")


def recognize_cmd(cmd):# занимается нечётким поиском команды
	RC = {'cmd': '', 'percent': 0}
	for c,v in opts['cmds'].items(): # прогоняем все соответствия сказанного с ячейкой cmds
		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']: # если выбранное совпадает, то выбираем этот вариант
				RC['cmd'] = c
				RC['percent'] = vrt

	return RC

def execute_cmd(cmd):
	if cmd == "ctime":
		now = datetime.datetime.now()
		speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
	elif cmd == "joke":
		speak("Колобок повесился, хехехех")
	elif cmd == "stop":
		speak("Принял, заканчиваю работу")
		sys.exit()
	else:
		speak("В моей базе данных нет такой команды")

# Запуск
speak_engine = pyttsx3.init()

voices = speak_engine.getProperty("voices")
speak_engine.setProperty('voice', voices[4].id)

speak("Добрый день")

#Запуск программы
r = sr.Recognizer()
m = sr.Microphone(device_index=1) # active microphone index

try:
    while True:
      with m as source:
        audio = r.listen(source)
      callback(r, audio)

except KeyboardInterrupt as e:
    print("Голосовой ассистент был остановлен вручную")
    sys.exit()