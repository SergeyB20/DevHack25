from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, ParseMode
from datetime import datetime
import time, random, sqlite3, os
from forms import Form
from config import *


TOKEN =TOKEN_BOT 
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = sqlite3.connect('server.db')
sql = db.cursor()



# НАЧАЛО, СОХРАНЕНИЕ ID ПОЛЬЗОВАТЕЛЯ В БД
@dp.message_handler(commands=['start'])
async def StartFunction(message: types.Message):
    user_id = message.from_user.id

    if user_id == 809727326:
        await message.answer(f'<b>Вы авторизованы как служба поддержки!\n</b> <i> Что-бы отвечать пользователю на заднные вопросы, вводите ответ по данному шаблону\n\n[номер пользователя]\n[текст сообщения]</i>', parse_mode=ParseMode.HTML)
        await Form.support.set()
    
    else:
        sql.execute(f"INSERT INTO users (ID) VALUES ({user_id})")
        db.commit()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'студент', resize_keyboard=True)
        btn1 = types.KeyboardButton(text=f'преподаватель', resize_keyboard=True)
        keyboard.add(btn, btn1)

        await bot.send_message(message.chat.id, 'Привет 👋, перед использованием тебе нужно зарегистрироваться!\nКем ты являешься? \n[студент/преподаватель]', reply_markup=keyboard)
        await Form.category.set()

# СОХРАНЕНИЕ КАТЕГОРИИ ПОЛЬЗОВАТЕЛЯ В БД (СТУДЕНТ ИЛИ ПРЕПОДАВАТЕЛЬ)
@dp.message_handler(state=Form.category)
async def SetCategory(message: types.Message):
    user_id = message.from_user.id
    msg = message.text

    if msg.lower() == 'студент':
        sql.execute(f"UPDATE users SET CATEGORY='{msg.lower()}' WHERE ID={user_id}")
        db.commit()
        await message.answer('✏️Укажите свою группу')
        await Form.NumGroup.set()

    if msg.lower() == 'преподаватель':
        sql.execute(f"UPDATE users SET CATEGORY='{msg.lower()}' WHERE ID={user_id}")
        db.commit()
        await message.answer('✏️Введите ваше ФИО [Иванов И.И]')
        await Form.NumGroup.set()

# СОХРАНЕНИЕ НОМЕРА ГРУППЫ/ФИО ПОЛЬЗОВАТЕЛЯ В БД
@dp.message_handler(state=Form.NumGroup)
async def SetNumGroup(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    sql.execute(f"UPDATE users SET NUMGROUP='{msg.lower()}' WHERE ID={user_id}")
    db.commit()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text=f'Да')
    btn1 = types.KeyboardButton(text=f'Нет')
    keyboard.add(btn,btn1)

    await message.answer('Вы согласны на получение уведомлений об изменениях в расписании?', reply_markup=keyboard)
    await Form.Mailing.set()


# ВНОС В БД РАЗРЕШЕНИЕ О РАССЫЛКЕ, ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРЕПОД ПЕРЕВОДИТ ЕГО К ВВОДУ КЛЮЧА ДОСТУПА
@dp.message_handler(state=Form.Mailing)
async def SetMailing(message: types.Message):
    user_id = message.from_user.id
    msg = message.text

    if msg.lower() == 'да':
        sql.execute(f"UPDATE users SET MAILING={1} WHERE ID={user_id}")
        db.commit()
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Пары {str(NumGroup[0]).upper()}')
            btn1 = types.KeyboardButton(text=f'Пары на неделю {str(NumGroup[0]).upper()}')
            btn2 = types.KeyboardButton(text=f'Помощь/FAQ')
            btn3 = types.KeyboardButton(text=f'Планшетка {NumGroup[0].upper()}')
            keyboard.add(btn, btn1, btn2, btn3)

        for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
            category = category[0]

        if category.lower() == 'преподаватель':
            await message.answer('Введите код доступа')
            await Form.TeachPass.set()
        else:
            await message.answer_sticker(sticker='https://github.com/TelegramBots/book/raw/master/src/docs/sticker-fred.webp')
            await message.answer('На этом всё, регистрация окончена!', reply_markup=keyboard)
            await Form.Meny.set()

    if msg.lower() == 'нет':
        sql.execute(f"UPDATE users SET MAILING={0} WHERE ID={user_id}")
        db.commit()

        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Пары {str(NumGroup[0]).upper()}')
            btn1 = types.KeyboardButton(text=f'Пары на неделю {str(NumGroup[0]).upper()}')
            btn2 = types.KeyboardButton(text=f'Помощь/FAQ')
            btn3 = types.KeyboardButton(text=f'Планшетка {str(NumGroup[0]).upper()}')
            keyboard.add(btn, btn1, btn2, btn3)

        await message.answer('На этом всё, регистрация окончена!', reply_markup=keyboard)
        await Form.Meny.set()


# ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРЕПОД, ОН ВВОДИТ КЛЮЧ ДОСТУПА И ПОЛУЧАЕТ ВСЕ ФУНКЦИИ
@dp.message_handler(state=Form.TeachPass)
async def SetTeachPass(message: types.Message):
    user_id = message.from_user.id
    msg = message.text

    if msg == '123':
        for FullName in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            FullName = FullName[0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Пары {FullName.upper()}')
        btn1 = types.KeyboardButton(text=f'Пары на неделю {FullName.upper()}')
        btn2 = types.KeyboardButton(text=f'Помощь/FAQ')
        btn3 = types.KeyboardButton(text=f'Планшетка {str(FullName).upper()}')
        keyboard.add(btn, btn1, btn2, btn3)
        await message.answer('Отлично, авторизация прошла успешно!\nВам доступны все функции', reply_markup=keyboard)
        await Form.Meny.set()
    else:
        await message.answer('Похоже вы что-то указали неправильно, попробуйте еще раз!')




# МЕНЮ, ОБРАБОТКА СООБЩЕНИЙ/КОМАНД ОТ ПОЛЬЗОВАТЕЛЯ
@dp.message_handler(state=Form.Meny)
async def SetMailing(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    
    for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
        category = category[0]
        
    if (len(msg.lower().split(' ')) == 2) and (msg.lower().split(' ')[0] == 'пары') or (len(msg.lower().split(' ')) == 3) and (msg.lower().split(' ')[0] == 'пары'):
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            NumGroup = NumGroup[0] #номер группы или ФИО
        # ФУНКЦИЯ ВЫВОДА РАСПИСАНИЯ НА ДВА ДНЯ (ГРУППЫ/ПРЕПОДА)
        await message.answer('пары на 2 дня')

    if (len(msg.lower().split(' ')) == 4) and (msg.lower().split(' ')[1] == 'на') or (len(msg.lower().split(' ')) == 5) and (msg.lower().split(' ')[0] == 'пары'):
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            NumGroup = NumGroup[0]#номер группы или ФИО
        try:
            StudentParser(user_id=user_id, NumGroup=msg.split(' ')[-1].upper())
            with open(f'result/{user_id}.txt', encoding='utf-8') as doc:
                    await message.answer(doc.read())
        except:
            ParserTeacher(user_id=user_id, fullname=f'{msg.split(" ")[-2]} {msg.split(" ")[-1]}')
            with open(f'result/{user_id}.txt', encoding='utf-8') as doc:
                    await message.answer(doc.read())

    if msg.lower().split(' ')[0] == 'планшетка':
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            NumGroup = NumGroup[0]#номер группы или ФИО

        # ДОБАВИТЬ ПАРСЕР ПЛАНШЕТКИ (ДЛЯ ГРУППЫ/ДЛЯ ПРЕПОДА)
        await message.answer('расписание на сегодня с планшетки')

    if msg.lower() == 'звонки':
        await message.answer(bells, parse_mode=ParseMode.HTML)

    if msg.lower() == 'регистрация':
        await message.answer('Кем ты являешься? \n[студент/преподаватель]')
        await Form.category.set()
    
    if msg.lower().split(' ')[0] == 'уведомления':
        sql.execute(f"UPDATE users SET MAILING={1} WHERE ID={user_id}")
        db.commit()
        await message.answer('Уведомления включены!')

    if msg.lower() == 'отписаться':
        sql.execute(f"UPDATE users SET MAILING={0} WHERE ID={user_id}")
        db.commit()
        await message.answer('Уведомления отключены!')

    if (msg.lower() == 'помощь/faq') and (category == 'студент'):
        await message.answer(ManStud)

    if (msg.lower() == 'помощь/faq') and (category == 'преподаватель'):
        await message.answer(ManTeach)

    if msg.lower() == 'контактная информация':
        await message.answer('Текст контактной информации')

    if msg.lower() == 'режим работы':
        await message.answer(OperatingMode, parse_mode=ParseMode.HTML)

    if msg.lower() == 'поддержка':
        await message.answer('<i>Введите ваше обращение/задайте интересующие вас вопросы...</i>', parse_mode=ParseMode.HTML)
        await Form.support_ask.set()

    if (len(msg.lower().split(' ')) == 3) and (msg.lower().split(' ')[0] == 'учебный'):
        content = msg.split(' ')
        with open(f'TEXT/AcademicPlan/{content[-1].split("-")[0].upper()}.pdf', 'rb') as doc:
            await message.answer_document(doc, caption=f'Учебный план для группы {content[-1]}')

    if msg.lower() == 'заявления':
        markup = types.InlineKeyboardMarkup(row_width=True)
        lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://drive.google.com/drive/folders/1-l17za1XrEvsE4JndjJG9k3zGYnCN4r4') 
        markup.add(lk1)
        await message.answer('<i> Все доступные заявления для студентов и преподавателей </i>', reply_markup=markup, parse_mode=ParseMode.HTML)

    if msg.lower() == 'заметка':
        if str(category).lower() == 'преподаватель':
            await message.answer('<b>Заполните по данному примеру:</b>\n\n<i>[дата дд.мм.гггг]\n[группа/преподаватель]\n[предмет:]\n<b> текст сообщения </b>  </i>', parse_mode=ParseMode.HTML)
            await Form.AddNote.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

    if msg.lower() == 'сообщение':
        if str(category).lower() == 'преподаватель':
            await message.answer('<b>Заполните по данному примеру:</b>\n\n<i>[группа/преподаватель/внимание]\n<b> текст сообщения </b>  </i>', parse_mode=ParseMode.HTML)
            await Form.notification.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

    if (len(msg.lower().split(' ')) == 2) and (msg.lower().split(' ')[0] == 'заметка'):
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            for content in sql.execute(f"SELECT CONTENTS FROM tasks WHERE DATE='{msg.lower().split(' ')[1]}' AND NUMGROUP='{NumGroup[0].lower()}' "):
                msg = str(content[0]).replace('/n', '\n')
                print(msg)
                await message.answer(msg)

    if (len(msg.lower().split(' ')) == 3) and (msg.lower().split(' ')[0] == 'контакт'):
        msg = msg.lower().split(" ")
        for PhoneNumber in sql.execute(f"SELECT PHONENUMBER FROM contacts WHERE FULLNAME='{msg[1]} {msg[2]}'"):
            for Telegram in sql.execute(f"SELECT TELEGRAM FROM contacts WHERE FULLNAME='{msg[1]} {msg[2]}'"):
                for email in sql.execute(f"SELECT MAIL FROM contacts WHERE FULLNAME='{msg[1]} {msg[2]}'"):
                    for fio in sql.execute(f"SELECT FIO FROM contacts WHERE FULLNAME='{msg[1]} {msg[2]}'"):
                        await message.answer(f'<b>{fio[0]}</b>\n\nтелефон - {PhoneNumber[0]}\nТелеграм - {Telegram[0]}\n Почта - {email[0]}', parse_mode=ParseMode.HTML)

    if (msg.lower().split(' ')[0] == 'добавить') and (msg.lower().split(' ')[1] == 'контакт'):
        for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
            category = category[0]

        if category.lower() == 'преподаватель':
            await message.answer('<b>Заполните по данному примеру:</b>\n\n<i>[ФИО]\n[Номер телефона]\n[Телеграм]\n[Почта]\n  </i>', parse_mode=ParseMode.HTML)
            sql.execute(f"INSERT INTO contacts (FULLNAME) VALUES ('{msg.lower().split(' ')[-1]}')")
            await Form.addcontacts.set()
        else:
            await message.answer('У вас нет доступа к данной функции!')


@dp.message_handler(state=Form.addcontacts)
async def AddNote(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    msg = msg.split('\n')
    sql.execute(f"INSERT INTO contacts (FULLNAME, FIO, PHONENUMBER,TELEGRAM, MAIL) VALUES ('{msg[0].lower()}', '{msg[1]}', '{msg[2]}', '{msg[3]}' , '{msg[4]}')")
    db.commit()

    await message.answer('<i>Контакты успешно добавлены, вы были переведены в меню...</i>', parse_mode=ParseMode.HTML)
    await Form.Meny.set()


@dp.message_handler(state=Form.AddNote)
async def AddNote(message: types.Message):
    msg = message.text

    content = msg.split('\n')
    try:
        for contents in sql.execute(f"SELECT CONTENTS FROM tasks WHERE DATE='{content[0]}' AND NUMGROUP='{content[1].lower()}' "):
            sql.execute(f"UPDATE tasks SET CONTENTS='{f'{contents[0]} /n {content[-2]}{content[-1]}'}' WHERE DATE='{content[0]}'AND NUMGROUP='{content[1].lower()}' ")
    except:
        sql.execute(f"INSERT INTO tasks (DATE, NUMGROUP, CONTENTS) VALUES ('{content[0]}', '{content[1].lower()}', '{content[-2]}{content[-1]}')")
    finally:
        db.commit()
        await message.answer('<i>Заметка добавлена, вы были переведены в меню...</i>', parse_mode=ParseMode.HTML)
        await Form.Meny.set()

@dp.message_handler(state=Form.notification)
async def AddNote(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    msg = message.text
    for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
        FullName = NumGroup[0]

    content = msg.split('\n')
    if content[0].lower() == 'внимание ':
        content.pop(0)
        msg = ''.join(content)
        print(msg)
        for i in sql.execute(f"SELECT ID FROM users WHERE MAILING={1}"):
            print(i[0])
            await bot.send_message(i[0], f"<a href='https://t.me/{username}'>{FullName}</a>\n{msg}", parse_mode=ParseMode.HTML)

    else:
        print(content[0].lower())
        for UserID in sql.execute(f"SELECT ID FROM users WHERE NUMGROUP='{content[0].lower()}' "): 
            for mailing in sql.execute(f"SELECT MAILING FROM users WHERE ID={UserID[0]}"):
                print(UserID[0])
                print(mailing)
                content.pop(0)
                msg = ''.join(content)
                if mailing[0] == 1:
                    await bot.send_message(UserID[0], f"<a href='https://t.me/{username}'>{FullName}</a>\n{msg}", parse_mode=ParseMode.HTML)
       
    db.commit()
    await message.answer('<i>Сообщения отправлены, вы были переведены в меню...</i>', parse_mode=ParseMode.HTML)
    await Form.Meny.set()


@dp.message_handler(state=Form.support_ask)
async def AddNote(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    await bot.send_message(809727326, f'{user_id}\n\n{msg}')
    await message.answer('<i>Обращение отправлено, вы были переведены в меню...</i>', parse_mode=ParseMode.HTML)
    await Form.Meny.set()

@dp.message_handler(state=Form.support)
async def AddNote(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    msg = msg.split('\n')
    await bot.send_message(msg[0], f'Поддержка...\n\n{msg[1]}')
    await message.answer('<i>Ответ отправлен, вы были переведены в меню...</i>', parse_mode=ParseMode.HTML)
    await Form.support.set()



if __name__ =='__main__':
    executor.start_polling(dp)