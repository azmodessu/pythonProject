import telebot
import webbrowser
from telebot import types
import sneakers
import Winter_shoes
import gumshoes
import sqlite3 as sq

bot = telebot.TeleBot('6629859628:AAFvORL4yJ_HuOFmssrTQwEN4a7ulhgMN8s')

markup_inline_sneakers = types.InlineKeyboardMarkup()
button_next_sneakers = types.InlineKeyboardButton('Следующий товар', callback_data='next_sneakers')
markup_inline_sneakers.add(button_next_sneakers)

markup_inline_wintershoes = types.InlineKeyboardMarkup()
button_next_wintershoes = types.InlineKeyboardButton('Следующий товар', callback_data='next_wintershoes')
markup_inline_wintershoes.add(button_next_wintershoes)

markup_inline_gumshoes = types.InlineKeyboardMarkup()
button_next_gumshoes = types.InlineKeyboardButton('Следующий товар', callback_data='next_gumshoes')
markup_inline_gumshoes.add(button_next_gumshoes)

# counter_all = 0
@bot.message_handler(commands=['start']) #обработки команды старт
def start(message):
    markup_outline = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_choose = types.KeyboardButton('Выбор категории')
    button_site = types.KeyboardButton('Перейти на сайт магазина')
    markup_outline.add(button_choose, button_site)

    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! \nЯ могу помочь тебе с выбором '
                                      f'обуви на сайте SneakerHead!</b>',
                     parse_mode='html', reply_markup=markup_outline)

@bot.message_handler(content_types=['text'])
def func(message):
    counter = 0
    if(message.text == 'Перейти на сайт магазина'):
        bot.send_message(message.chat.id, 'Выполняется переход на сайт магазина (https://sneakerhead.ru)')
        webbrowser.open('https://sneakerhead.ru')

    elif(message.text == 'Выбор категории'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_sneakers = types.KeyboardButton('Кроссовки')
        button_winter_shoes = types.KeyboardButton('Зимняя обувь')
        button_gumshoes = types.KeyboardButton('Кеды')
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup.add(button_sneakers, button_winter_shoes, button_gumshoes, button_return)
        bot.send_message(message.chat.id, 'Какая категория Вас интересует?', reply_markup=markup)

    elif(message.text == 'Вернуться в главное меню'):
        markup_outline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_choose = types.KeyboardButton('Выбор категории')
        button_site = types.KeyboardButton('Перейти на сайт магазина')
        markup_outline.add(button_choose, button_site)
        bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! \nЯ могу помочь тебе с выбором '
                                          f'обуви на сайте SneakerHead!</b>',
                         parse_mode='html', reply_markup=markup_outline)

    elif(message.text == 'Кроссовки'):
        bot.send_message(message.chat.id, 'Идёт сбор информации, пожалуйста подождите')
        sneakers.export()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_xlsx = types.KeyboardButton('Таблица с кроссовками')

        button_database = types.KeyboardButton('Выгрузка из базы данных с кроссовками')

        markup.add(button_return, button_xlsx, button_database)
        bot.send_message(message.chat.id, 'В каком виде предоставить информацию?', reply_markup=markup)

    elif(message.text == 'Таблица с кроссовками'):
        markup_ifxslx = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup_ifxslx.add(button_return)
        file = open('./sneakers.xlsx', 'rb')
        bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, 'Таблица с полученными данными', reply_markup=markup_ifxslx)


    elif(message.text == 'Выгрузка из базы данных с кроссовками'):
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_next = types.KeyboardButton('Следующая модель кроссовок')
        markup_ifdatabase.add(button_return, button_next)

        # Устанавливаем соединение с базой данных
        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM sneakers')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)
        bot.send_message(message.chat.id, str(users_list[counter]).replace("'", "").replace("{", "").replace("}", ""), reply_markup=markup_inline_sneakers)

    elif(message.text == 'Следующая модель кроссовок'):
        counter += 1
        markup_innernext = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_innernext = types.KeyboardButton('Следующая модель')

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM sneakers')
        users = cursor.fetchall()

        # Выводим результаты
        # for user in users:
        #     print(user[0])
        # print(len(users))

        # Закрываем соединение
        con.close()
        # Устанавливаем соединение с базой данных
        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM sneakers')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)
        bot.send_message(message.chat.id, str(users_list[counter]), reply_markup=markup_innernext)


    elif (message.text == 'Зимняя обувь'):
        bot.send_message(message.chat.id, 'Идёт сбор информации, пожалуйста подождите')
        Winter_shoes.export()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_xlsx = types.KeyboardButton('Таблица с зимней обувью')
        button_database = types.KeyboardButton('Выгрузка из базы данных с зимней обувью')
        markup.add(button_return, button_xlsx, button_database)
        bot.send_message(message.chat.id, 'В каком виде предоставить информацию?', reply_markup=markup)

    elif (message.text == 'Таблица с зимней обувью'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup.add(button_return)
        file = open('./wintershoes.xlsx', 'rb')
        bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, 'Таблица с полученными данными', reply_markup=markup)

    elif (message.text == 'Выгрузка из базы данных с зимней обувью'):
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_next = types.KeyboardButton('Следующая модель зимней обуви')
        markup_ifdatabase.add(button_return, button_next)

        # markup_inline = types.InlineKeyboardMarkup()
        # button = types.InlineKeyboardButton('Next', callback_data='next')
        # markup_inline.add(button)

        # Устанавливаем соединение с базой данных
        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM winter_shoes')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)
        bot.send_message(message.chat.id, str(users_list[counter]).replace("'", "").replace("{", "").replace("}", ""),
                         reply_markup=markup_inline_wintershoes)

    elif (message.text == 'Кеды'):
        bot.send_message(message.chat.id, 'Идёт сбор информации, пожалуйста подождите')
        gumshoes.export()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_xlsx = types.KeyboardButton('Таблица с кедами')
        button_database = types.KeyboardButton('Выгрузка из базы данных с кедами')
        markup.add(button_return, button_xlsx, button_database)
        bot.send_message(message.chat.id, 'В каком виде предоставить информацию?', reply_markup=markup)

    elif (message.text == 'Таблица с кедами'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup.add(button_return)
        file = open('./gumshoes.xlsx', 'rb')
        bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, 'Таблица с полученными данными', reply_markup=markup)

    elif (message.text == 'Выгрузка из базы данных с кедами'):
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_next = types.KeyboardButton('Следующая модель кед')
        markup_ifdatabase.add(button_return, button_next)

        # Устанавливаем соединение с базой данных
        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM gumshoes')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)
        bot.send_message(message.chat.id, str(users_list[counter]).replace("'", "").replace("{", "").replace("}", ""),
                         reply_markup=markup_inline_gumshoes)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b><em>Данный бот основывается на <u>парсинге</u> данных различных категорий '
                                      'товаров с сайта SneakerHead. Полученная информация добавляется в '
                                      '<u>базу данных</u>, доступ к которой предоставляется пользователю.</em></b>',
                     parse_mode='html')

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://sneakerhead.ru')

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message('Данный бот не поддерживает работу с фотографиями.')

k = 0
def counter():
    # s = k + 1
    # return s

    global k
    k += 1
@bot.callback_query_handler(func=lambda callback:True)
def callback_next(callback):
    if callback.data == 'next_sneakers':
        counter()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM sneakers')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)

        bot.send_message(callback.message.chat.id, str(users_list[k]).replace("'", "").replace("{", "").replace("}", "").replace(", ", "\n"), reply_markup=markup_inline_sneakers)

    if callback.data == 'next_wintershoes':
        counter()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM winter_shoes')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)

        bot.send_message(callback.message.chat.id, str(users_list[k]).replace("'", "").replace("{", "").replace("}", "").replace(", ", "\n"), reply_markup=markup_inline_wintershoes)

    if callback.data == 'next_gumshoes':
        counter()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM gumshoes')
        users = cursor.fetchall()
        con.close()

        users_list = []
        for user in users:
            user_dict = {
                'Название': str(user[0]),
                'Цена': str(user[1]),
                'Картинка': str(user[2])
            }
            users_list.append(user_dict)

        bot.send_message(callback.message.chat.id, str(users_list[k]).replace("'", "").replace("{", "").replace("}", "").replace(", ", "\n"), reply_markup=markup_inline_gumshoes)
#bot.polling(none_stop=True) #бесконечная работа бота
