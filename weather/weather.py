# -*- coding: utf-8 -*-
import time
from tkinter import Tk, W, E, BOTH
from tkinter.ttk import Frame, Label, Style

import requests


class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.parent.title("Weather Online")

        Style().configure("TFrame", background='gray')

        Style().configure("TLabel", padding=(0, 5, 0, 5), background='gray',
                          font='serif 12', foreground='white')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2)
        self.rowconfigure(3)
        self.rowconfigure(4)
        self.rowconfigure(5)
        self.rowconfigure(6)
        self.rowconfigure(7)
        self.rowconfigure(8)
        self.rowconfigure(9)
        self.rowconfigure(10)

        # Title
        self.city = Label(self, text='Санкт-Петербург', font='serif 40')
        self.city.grid(row=0, columnspan=3, column=0, sticky=W)

        self.degrees = Label(self, text="-3\u2103", font='serif 40')
        self.degrees.grid(row=0, columnspan=2, column=3, sticky=E)

        # Current info
        self.weather = Label(self, text='Clouds')
        self.weather.grid(row=1, columnspan=2, column=0, sticky=W, padx=10)

        self.wind = Label(self, text='Wind 2 m/s, NW')
        self.wind.grid(row=2, columnspan=2, column=0, sticky=W, padx=10)

        self.humidity = Label(self, text='Humidity 75%')
        self.humidity.grid(row=3, columnspan=2, column=0, sticky=W, padx=10)

        self.pressure = Label(self, text='Pressure 763 mm', )
        self.pressure.grid(row=4, columnspan=2, column=0, sticky=W, padx=10)

        # Title for future weather
        self.title_future = Label(self, text='Прогноз на следущие дни')
        self.title_future.grid(row=7, columnspan=5, column=0)

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

    url_forecast = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}&units=metric&lang={}'. \
        format(city_name, country_code, appid, lang)

    weather = requests.get(url=url_weather).json()
    forecast = requests.get(url=url_forecast).json()

    # Update current weather
    app.degrees['text'] = str(weather['main']['temp']) + chr(176)
    app.weather['text'] = weather['weather'][0]['description']
    try:
        app.wind['text'] = 'Ветер ' + str(weather['wind']['speed']) + 'м/с, ' + deg_to_compass(weather['wind']['deg'])
    except KeyError:
        if KeyError == 'deg':
            app.wind['text'] = 'Ветер ' + str(weather['wind']['speed']) + 'м/с'
        else:
            app.wind['text'] = deg_to_compass(weather['wind']['deg'])

    app.humidity['text'] = 'Влажность ' + str(weather['main']['humidity']) + '%'
    app.pressure['text'] = 'Давление ' + str(round(weather['main']['pressure'] * hpatomm)) + 'мм'

    # Update forecast
    list = forecast['list']
    forecast_days = []
    for period in list:
        tm = time.localtime(period['dt'])
        day_of_week = [('ПН', 'Понедельник'), ('ВТ', 'Вторник'), ('СР', 'Среда'),
                       ('ЧТ', 'Четверг'), ('ПТ', 'Пятница'), ('СБ', 'Суббота'), ('ВС', 'Воскреснье')]
        date = str(day_of_week[tm.tm_wday][1])
        last = len(forecast_days) - 1

        # Определение максимальной и минимальной температуры и добавления нового дня к прогнозу
        if last == -1 or forecast_days[last]['date'] != date:
            forecast_days.append({'date': date, 'weather': period['weather'][0]['main'],
                                  'min_temp': round(period['main']['temp_min']),
                                  'max_temp': round(period['main']['temp_max'])})
        else:
            if forecast_days[last]['min_temp'] > round(period['main']['temp_min']):
                forecast_days[last]['min_temp'] = round(period['main']['temp_min'])

            if forecast_days[last]['max_temp'] < round(period['main']['temp_max']):
                forecast_days[last]['max_temp'] = round(period['main']['temp_max'])

        # Определение погоды днём
        if tm.tm_hour == 15:
            forecast_days[last]['weather'] = period['weather'][0]['main']

        # # Данные о прогнозе погоды
        # for key in period.keys():
        #     if key == 'dt':
        #         print(time.strftime("%H:%M %d/%m/%y", time.localtime(period[key])))
        #     else:
        #         print(str(key) + ': ' + str(period[key]))
        # print()

    for col in range(1, 4):
        period = list[col-1]
        degrees = str(int(period['main']['temp'])) + chr(176)
        weather = period['weather'][0]['description']
        dt = time.strftime("%H:%M", time.localtime(period['dt']))
        wind = str(period['wind']['speed']) + 'м/с, ' + deg_to_compass(period['wind']['deg'])
        press_and_hum = str(round(period['main']['pressure'] * hpatomm)) + 'мм, ' + \
                                str(period['main']['humidity']) + '%'

        Label(app, text=degrees, font='serif 30').grid(row=1, rowspan=2, column=col+1)
        Label(app, text=weather).grid(row=3, column=col+1)
        Label(app, text=dt).grid(row=4, column=col+1)
        Label(app, text=wind).grid(row=5, column=col+1)
        Label(app, text=press_and_hum).grid(row=6, column=col+1)

    for i in range(1, len(forecast_days)):
        day = forecast_days[i]
        temp = str(day['min_temp']) + '...' + str(day['max_temp'])
        col = i - 1
        # print(day)
        Label(app, text=day['date']).grid(row=8, column=col)
        Label(app, text=day['weather']).grid(row=9, column=col)
        Label(app, text=temp).grid(row=10, column=col)


def deg_to_compass(degrees):
    val = int((degrees / 45) + .5)
    arr = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    return arr[(val % 8)]


def center_window(window):
    w = 600
    h = 400

    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()

    x = (sw - w) / 2
    y = (sh - h) / 2
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


root = Tk()
root.overrideredirect(True)
app = MainFrame(root)
app.after_idle(info_weather)
root.mainloop()
