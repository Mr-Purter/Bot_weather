from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from telebot import types
import requests
import datetime
from random import randint

                                            #Токены
OWM = 'f189a540bc3a8995542e3e4637203d3f'
bot = Bot(token="")
dp = Dispatcher(bot)

                                            #Типы погоды
type_weather = {
    "Clear": "Ясно ☀",
    "Clouds": "Облачно ☁",
    "Overcast clouds": "Облачно ☁",
    "Drizzle": "Дождь 🌧",
    "Rain": "Дождь 🌧",
    "Thunderstorm": "Гроза ⛈",
    "Moderate rain": "Дождь 🌧",
    "Mist": "Туман 🌫️",
    "Snow": "Снег ❄"}

                                            #Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    p = open('cvb.jpg', 'rb')
    await bot.send_message(message.from_user.id,
                           'Привет!\nЯ бот синоптик. Напиши мне свой город и я расскажу всё информацию о погоде. Надеюсь тебе понравится моя работа.'
                           '\nЕсли возникнут проблемы, пиши моему разработчику @purter23.'
                           ' Удачи :)')
    await bot.send_photo(message.from_user.id, p)

                                            #Команда /date
@dp.message_handler(commands=['date'])
async def date(message: types.Message):
    today = datetime.datetime.today()
    await bot.send_message(message.from_user.id, today.strftime("Дата: %d.%m.%Y \nВремя: %H:%M:%S"));


                                            #Команда /Game
@dp.message_handler(commands=['game'])
async def game(message: types.Message):
    ch_chel = randint(0, 100)
    ch_bot = randint(0, 100)
    if int(ch_bot) > int(ch_chel):
        await bot.send_message(message.from_user.id, 'Вы проиграли!!!!'
                                                     '\n Бот выбил: ' + str(ch_bot) +
                                                     '\n Вы выбили: ' + str(ch_chel))

    elif int(ch_bot) < int(ch_chel):
        await bot.send_message(message.from_user.id, 'Вы выйграли!!!!'
                                                     '\n Бот выбил: ' + str(ch_bot) +
                                                     '\n Вы выбили: ' + str(ch_chel))


    else:
        await bot.send_message(message.from_user.id, 'Ничья!!!!'
                                                     '\n Бот выбил: ' + str(ch_bot) +
                                                     '\n Вы выбили: ' + str(ch_chel))

                                            #Команда /help
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, '-------------------Команды--------------------'
                                                 '\n 1./start - Стартовое сообщение'
                                                 '\n 2./help - Команды'
                                                 '\n 3./date - Дата'
                                                 '\n 4./game - Игра на рандом число с ботом(0-100)')

                                        #Поиск информации о погоде
@dp.message_handler()
async def find_weather(message: types.Message):
    try:                              #Запрос
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={OWM}&units=metric")
        data = r.json()
                                #Берём определённые данные
        temp = data['main']['temp']          #Температура
        fl_temp = data['main']['feels_like'] #Температура (ощущение)
        vlag = data['main']['humidity']      #Влажнсть
        dav = data['main']['pressure']       #Давление
        vis = data['visibility']             #Дальность видимости
        wind = data['wind']['speed']         #Скорость ветра (м/с)
        wind_deg = data['wind']['deg']       #Направление ветра


        if data["weather"][0]["main"] in type_weather:
            tp_weat = type_weather[data["weather"][0]["main"]]
        else:
            tp_weat = ""

        # Дождь идет или нет
        if tp_weat == 'Дождь 🌧':
            zont = 'идет'
        else:
            zont = '---'
                                        #Вывод инфоримации в сообщении
            await bot.send_message(message.from_user.id, 'Температура: ' + str(temp) + '°C' + ' (' + str(tp_weat) + ')'
                               '\nОщущается как: ' + str(fl_temp) + '°C' +
                               '\nДождь: ' + str(zont) +
                               '\nВлажность: ' + str(vlag) + ' %' +
                               '\nДавление: ' + str(dav) + ' ГПа' +
                               '\nВидимость: ' + str(vis) + ' М' +
                               '\nВетер: ' + str(wind) + ' М/с (Направление: ' + str(wind_deg) + '°)')





    except Exception:
        await bot.send_message(message.from_user.id, "Неверное название города!!!!!!")


executor.start_polling(dp)
