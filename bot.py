import telebot
import webbrowser
from telebot import types
import sneakers
import Winter_shoes
import gumshoes
import sqlite3 as sq
import added

bot = telebot.TeleBot('6629859628:AAFvORL4yJ_HuOFmssrTQwEN4a7ulhgMN8s')

markup_inline_sneakers = types.InlineKeyboardMarkup()
button_next_sneakers = types.InlineKeyboardButton('Следующий товар', callback_data='next_sneakers')
button_add_sneakers = types.InlineKeyboardButton('В избранное', callback_data='add')
markup_inline_sneakers.add(button_next_sneakers, button_add_sneakers)

markup_inline_wintershoes = types.InlineKeyboardMarkup()
button_next_wintershoes = types.InlineKeyboardButton('Следующий товар', callback_data='next_wintershoes')
button_add_wintershoes = types.InlineKeyboardButton('В избранное', callback_data='add')
markup_inline_wintershoes.add(button_next_wintershoes, button_add_wintershoes)

markup_inline_gumshoes = types.InlineKeyboardMarkup()
button_next_gumshoes = types.InlineKeyboardButton('Следующий товар', callback_data='next_gumshoes')
button_add_gumshoes = types.InlineKeyboardButton('В избранное', callback_data='add')
markup_inline_gumshoes.add(button_next_gumshoes, button_add_gumshoes)

all_shoes_list = []
added_shoes = []

k_all = -1


def counter_all():
    global k_all
    k_all += 1


k_sneakers = -1


def counter_sneakers():
    global k_sneakers
    k_sneakers += 1


k_wintershoes = -1


def counter_wintershoes():
    global k_wintershoes
    k_wintershoes += 1


k_gumshoes = -1


def counter_gumshoes():
    global k_gumshoes
    k_gumshoes += 1


@bot.message_handler(commands=['start'])
def start(message):
    markup_outline = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_choose = types.KeyboardButton('Выбор категории')
    button_site = types.KeyboardButton('Перейти на сайт магазина')
    button_added = types.KeyboardButton('Посмотреть избранное')
    markup_outline.add(button_choose, button_site, button_added)

    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! \nЯ могу помочь тебе с выбором '
                                      f'обуви на сайте SneakerHead!</b>',
                     parse_mode='html', reply_markup=markup_outline)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == 'Перейти на сайт магазина'):
        bot.send_message(message.chat.id, 'Выполняется переход на сайт магазина (https://sneakerhead.ru)')
        webbrowser.open('https://sneakerhead.ru')

    elif (message.text == 'Выбор категории'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_sneakers = types.KeyboardButton('Кроссовки')
        button_winter_shoes = types.KeyboardButton('Зимняя обувь')
        button_gumshoes = types.KeyboardButton('Кеды')
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup.add(button_sneakers, button_winter_shoes, button_gumshoes, button_return)
        bot.send_message(message.chat.id, 'Какая категория Вас интересует?', reply_markup=markup)

    elif (message.text == 'Вернуться в главное меню'):
        markup_outline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_choose = types.KeyboardButton('Выбор категории')
        button_site = types.KeyboardButton('Перейти на сайт магазина')
        button_added = types.KeyboardButton('Посмотреть избранное')
        markup_outline.add(button_choose, button_site, button_added)
        bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! \nЯ могу помочь тебе с выбором '
                                          f'обуви на сайте SneakerHead!</b>',
                         parse_mode='html', reply_markup=markup_outline)

    elif (message.text == 'Посмотреть избранное'):
        added.export(added_shoes)

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM added_shoes')
        shoes_in_added = cursor.fetchall()
        con.close()

        shoes_in_added_list = []
        for shoe in shoes_in_added:
            shoes_in_added_list.append(shoe)

        bot.send_message(message.chat.id, (
            str(shoes_in_added_list).replace('(', '').replace(')', '').replace(',',
                                                                               '\n').replace('[', '').replace(']',
                                                                                                              '').replace(
                "'", '')))

    elif (message.text == 'Кроссовки'):
        bot.send_message(message.chat.id, 'Идёт сбор информации, пожалуйста подождите')
        sneakers.export()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        button_xlsx = types.KeyboardButton('Таблица с кроссовками')
        button_database = types.KeyboardButton('Выгрузка из базы данных с кроссовками')

        markup.add(button_return, button_xlsx, button_database)
        bot.send_message(message.chat.id, 'В каком виде предоставить информацию?', reply_markup=markup)

    elif (message.text == 'Таблица с кроссовками'):
        markup_ifxslx = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup_ifxslx.add(button_return)
        file = open('./sneakers.xlsx', 'rb')
        bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, 'Таблица с полученными данными', reply_markup=markup_ifxslx)

    elif (message.text == 'Выгрузка из базы данных с кроссовками'):
        counter_all()
        counter_sneakers()
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup_ifdatabase.add(button_return)

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM sneakers')
        sneakers_all = cursor.fetchall()
        con.close()

        sneakers_list = []
        for sneaker in sneakers_all:
            sneaker_dict = {
                'Название': str(sneaker[0]),
                'Цена': str(sneaker[1]),
                'Картинка': str(sneaker[2]),
                'Ссылка': str(sneaker[3])
            }
            sneakers_list.append(sneaker_dict)

        all_shoes_list.append(
            sneakers_list[k_sneakers]['Название'] + ' tabulation ' + sneakers_list[k_sneakers]['Ссылка'])
        bot.send_message(message.chat.id,
                         str(sneakers_list[k_sneakers]).replace("'", "").replace("{", "").replace("}", ""),
                         reply_markup=markup_inline_sneakers)

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
        counter_all()
        counter_wintershoes()
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup_ifdatabase.add(button_return)

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM winter_shoes')
        wintershoes_all = cursor.fetchall()
        con.close()

        wintershoes_list = []
        for wintershoe in wintershoes_all:
            wintershoe_dict = {
                'Название': str(wintershoe[0]),
                'Цена': str(wintershoe[1]),
                'Картинка': str(wintershoe[2]),
                'Ссылка': str(wintershoe[3])
            }
            wintershoes_list.append(wintershoe_dict)
        all_shoes_list.append(
            wintershoes_list[k_wintershoes]['Название'] + ' tabulation ' + wintershoes_list[k_wintershoes]['Ссылка'])
        bot.send_message(message.chat.id,
                         str(wintershoes_list[k_wintershoes]).replace("'", "").replace("{", "").replace("}", ""),
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
        counter_all()
        counter_gumshoes()
        markup_ifdatabase = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_return = types.KeyboardButton('Вернуться в главное меню')
        markup_ifdatabase.add(button_return)

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM gumshoes')
        gumshoes_all = cursor.fetchall()
        con.close()

        gumshoes_list = []
        for gumshoe in gumshoes_all:
            gumshoe_dict = {
                'Название': str(gumshoe[0]),
                'Цена': str(gumshoe[1]),
                'Картинка': str(gumshoe[2]),
                'Ссылка': str(gumshoe[3])
            }
            gumshoes_list.append(gumshoe_dict)
        all_shoes_list.append(
            gumshoes_list[k_gumshoes]['Название'] + ' tabulation ' + gumshoes_list[k_gumshoes]['Ссылка'])
        bot.send_message(message.chat.id,
                         str(gumshoes_list[k_gumshoes]).replace("'", "").replace("{", "").replace("}", ""),
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


@bot.callback_query_handler(func=lambda callback: True)
def callback_next(callback):
    if callback.data == 'next_sneakers':
        counter_all()
        counter_sneakers()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM sneakers')
        sneakers = cursor.fetchall()
        con.close()

        sneakers_list = []
        for sneaker in sneakers:
            sneakers_dict = {
                'Название': str(sneaker[0]),
                'Цена': str(sneaker[1]),
                'Картинка': str(sneaker[2]),
                'Ссылка': str(sneaker[3])
            }
            sneakers_list.append(sneakers_dict)

        all_shoes_list.append(
            sneakers_list[k_sneakers]['Название'] + ' tabulation ' + sneakers_list[k_sneakers]['Ссылка'])

        bot.send_message(callback.message.chat.id,
                         str(sneakers_list[k_sneakers]).replace("'", "").replace("{", "").replace("}", "").replace(", ",
                                                                                                                   "\n"),
                         reply_markup=markup_inline_sneakers)

    if callback.data == 'next_wintershoes':
        counter_all()
        counter_wintershoes()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM winter_shoes')
        wintershoes = cursor.fetchall()
        con.close()

        wintershoes_list = []
        for wintershoe in wintershoes:
            wintershoes_dict = {
                'Название': str(wintershoe[0]),
                'Цена': str(wintershoe[1]),
                'Картинка': str(wintershoe[2]),
                'Ссылка': str(wintershoe[3])
            }
            wintershoes_list.append(wintershoes_dict)

        all_shoes_list.append(
            wintershoes_list[k_wintershoes]['Название'] + ' tabulation ' + wintershoes_list[k_wintershoes]['Ссылка'])
        bot.send_message(callback.message.chat.id,
                         str(wintershoes_list[k_wintershoes]).replace("'", "").replace("{", "").replace("}",
                                                                                                        "").replace(
                             ", ", "\n"), reply_markup=markup_inline_wintershoes)

    if callback.data == 'next_gumshoes':
        counter_all()
        counter_gumshoes()

        con = sq.connect('sneakers.db')
        cursor = con.cursor()

        cursor.execute('SELECT * FROM gumshoes')
        gumshoes = cursor.fetchall()
        con.close()

        gumshoes_list = []
        for gumshoe in gumshoes:
            gumshoes_dict = {
                'Название': str(gumshoe[0]),
                'Цена': str(gumshoe[1]),
                'Картинка': str(gumshoe[2]),
                'Ссылка': str(gumshoe[3])
            }
            gumshoes_list.append(gumshoes_dict)

        all_shoes_list.append(
            gumshoes_list[k_gumshoes]['Название'] + ' tabulation ' + gumshoes_list[k_gumshoes]['Ссылка'])
        bot.send_message(callback.message.chat.id,
                         str(gumshoes_list[k_gumshoes]).replace("'", "").replace("{", "").replace("}", "").replace(", ",
                                                                                                                   "\n"),
                         reply_markup=markup_inline_gumshoes)

    if callback.data == 'add':
        print(all_shoes_list[k_all])
        added_shoes.append(all_shoes_list[k_all])
        print(added_shoes)
