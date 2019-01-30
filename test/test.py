# -*- coding: utf-8 -*-
import time
from tkinter import Tk, W, E, BOTH
from tkinter.ttk import Frame, Label, Style

import requests


class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.centerWindow()

    def centerWindow(self):
        w = 600
        h = 400

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):
        self.parent.title("Weather Online")

        Style().configure("TLabel", padding=(0, 5, 0, 5),
                          font='serif 14')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2)
        self.rowconfigure(3)
        self.rowconfigure(4)
        self.rowconfigure(5)
        self.rowconfigure(6)

        # Title
        self.city = Label(self, text='Санкт-Петербург', font='serif 40')
        self.city.grid(row=0, columnspan=3, column=0, sticky=W)
        self.degrees = Label(self, text="-3\u2103", font='serif 40')
        self.degrees.grid(row=0, column=3, sticky=E)

        # Current info
        self.weather = Label(self, text='Clouds')
        self.weather.grid(row=1, column=0, sticky=W, padx=10)
        self.wind = Label(self, text='Wind 2 m/s, NW')
        self.wind.grid(row=2, column=0, sticky=W, padx=10)
        self.humidity = Label(self, text='Humidity 75%')
        self.humidity.grid(row=3, column=0, sticky=W, padx=10)
        self.pressure = Label(self, text='Pressure 763 mm', )
        self.pressure.grid(row=4, column=0, sticky=W, padx=10)

        # Block future weather 1
        self.degrees1 = Label(self, text="-3\u2103", font='serif 30')
        self.degrees1.grid(row=1, rowspan=2, column=1)
        self.weather1 = Label(self, text='Clouds')
        self.weather1.grid(row=3, column=1)
        self.dt1 = Label(self, text='9.00-12.00')
        self.dt1.grid(row=4, column=1)
        self.wind1 = Label(self, text='2 m/s, NW')
        self.wind1.grid(row=5, column=1)
        self.presshum1 = Label(self, text='763 mm, 75%')
        self.presshum1.grid(row=6, column=1)

        # Block future weather 2
        self.degrees2 = Label(self, text="-3\u2103", font='serif 30')
        self.degrees2.grid(row=1, rowspan=2, column=2)
        self.weather2 = Label(self, text='Clouds')
        self.weather2.grid(row=3, column=2)
        self.dt2 = Label(self, text='9.00-12.00')
        self.dt2.grid(row=4, column=2)
        self.wind2 = Label(self, text='2 m/s, NW')
        self.wind2.grid(row=5, column=2)
        self.presshum2 = Label(self, text='763 mm, 75%')
        self.presshum2.grid(row=6, column=2)

        # Block future weather 3
        self.degrees3 = Label(self, text="-3\u2103", font='serif 30')
        self.degrees3.grid(row=1, rowspan=2, column=3)
        self.weather3 = Label(self, text='Clouds')
        self.weather3.grid(row=3, column=3)
        self.dt3 = Label(self, text='9.00-12.00')
        self.dt3.grid(row=4, column=3)
        self.wind3 = Label(self, text='2 m/s, NW')
        self.wind3.grid(row=5, column=3)
        self.presshum3 = Label(self, text='763 mm, 75%')
        self.presshum3.grid(row=6, column=3)

        self.pack(fill=BOTH, expand=True)


def info_weather():
    app.after(60000, info_weather)
    hpatomm = 0.7501

    lang = 'ru'
    country_code = 'RU'
    city_name = 'Sankt-Peterburg'
    city_name_ru = 'Санкт-Петербург'

    appid = '748e056a1080d9f870aa1fd88d49e416'

    url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units=metric&lang={}'. \
        format(city_name, country_code, appid, lang)

    url_forecast = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}&units=metric&lang={}&cnt=3'. \
        format(city_name, country_code, appid, lang)

    weather = requests.get(url=url_weather).json()
    forecast = requests.get(url=url_forecast).json()
    print(weather)
    print(forecast)

    # Update current weather
    app.degrees['text'] = str(weather['main']['temp']) + chr(176)
    app.weather['text'] = weather['weather'][0]['description']
    app.wind['text'] = 'Ветер ' + str(weather['wind']['speed']) + 'м/с, ' + degToCompass(weather['wind']['deg'])
    app.humidity['text'] = 'Влажность ' + str(weather['main']['humidity']) + '%'
    app.pressure['text'] = 'Давление ' + str(round(weather['main']['pressure'] * hpatomm, 2)) + 'мм'

    # Update forecast
    list = forecast['list']
    # First block
    first = list[0]
    app.degrees1['text'] = str(first['main']['temp']) + chr(176)
    app.weather1['text'] = first['weather'][0]['description']
    app.dt1['text'] = time.strftime("%H.%M", time.localtime(first['dt']))
    app.wind1['text'] = str(first['wind']['speed']) + 'м/с, ' + degToCompass(first['wind']['deg'])
    app.presshum1['text'] = str(round(first['main']['pressure'] * hpatomm, 2)) + 'мм, ' + \
                            str(first['main']['humidity']) + '%'

    # Second block
    second = list[1]
    app.degrees2['text'] = str(second['main']['temp']) + chr(176)
    app.weather2['text'] = second['weather'][0]['description']
    app.dt2['text'] = time.strftime("%H.%M", time.localtime(second['dt']))
    app.wind2['text'] = str(second['wind']['speed']) + 'м/с, ' + degToCompass(second['wind']['deg'])
    app.presshum2['text'] = str(round(second['main']['pressure'] * hpatomm, 2)) + 'мм, ' + \
                            str(second['main']['humidity']) + '%'

    # Third block
    third = list[2]
    app.degrees3['text'] = str(third['main']['temp']) + chr(176)
    app.weather3['text'] = third['weather'][0]['description']
    app.dt3['text'] = time.strftime("%H.%M", time.localtime(third['dt']))
    app.wind3['text'] = str(third['wind']['speed']) + 'м/с, ' + degToCompass(third['wind']['deg'])
    app.presshum3['text'] = str(round(third['main']['pressure'] * hpatomm, 2)) + 'мм, ' + \
                            str(third['main']['humidity']) + '%'


def degToCompass(degrees):
    val = int((degrees / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


root = Tk()
root.wm_resizable(600, 400)
app = MainFrame(root)
app.after_idle(info_weather)
root.mainloop()
