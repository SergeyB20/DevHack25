from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, ParseMode
from datetime import datetime
import time, random, sqlite3, os
from forms import Form
from settings import TG_BOT_TOKEN

TOKEN = TG_BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = sqlite3.connect('server.db')
sql = db.cursor()




@dp.message_handler(commands=['start'])
async def StartFunction(message: types.Message):
    user_id = message.from_user.id

    sql.execute(f"INSERT INTO users (ID) VALUES ({user_id})")
    db.commit()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text=f'студент', resize_keyboard=True)
    btn1 = types.KeyboardButton(text=f'преподаватель', resize_keyboard=True)
    keyboard.add(btn, btn1)

    await bot.send_message(message.chat.id, 'Привет, перед использованием тебе нужно зарегистрироваться!\nКем ты являешься? (студент/преподаватель)', reply_markup=keyboard)
    await Form.category.set()


@dp.message_handler(state=Form.category)
async def SetCategory(message: types.Message):
    user_id = message.from_user.id
    msg = message.text

    if msg.lower() == 'студент':
        sql.execute(f"UPDATE users SET CATEGORY='{msg.lower()}' WHERE ID={user_id}")
        db.commit()
        await message.answer('Введите номер группу')
        await Form.NumGroup.set()

    if msg.lower() == 'преподаватель':
        sql.execute(f"UPDATE users SET CATEGORY='{msg.lower()}' WHERE ID={user_id}")
        db.commit()
        await message.answer('Введите ваше фио (Иванов И.И)')
        await Form.NumGroup.set()

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
        keyboard.add(btn, btn1, btn2)
        await message.answer('Отлично у вас есть доступ преподавателя!', reply_markup=keyboard)
        await Form.Meny.set()
    else:
        await message.answer('Похоже вы что-то указали неправильно, попробуйте еще раз!')


@dp.message_handler(state=Form.Mailing)
async def SetMailing(message: types.Message):
    user_id = message.from_user.id
    msg = message.text

    if msg.lower() == 'да':
        sql.execute(f"UPDATE users SET MAILING='{1}' WHERE ID={user_id}")
        db.commit()
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Пары {str(NumGroup[0]).upper()}')
            btn1 = types.KeyboardButton(text=f'Пары на неделю {str(NumGroup[0]).upper()}')
            btn2 = types.KeyboardButton(text=f'Помощь/FAQ')
            keyboard.add(btn, btn1, btn2)

        for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
            category = category[0]

        if category.lower() == 'преподаватель':
            await message.answer('Введите код доступа')
            await Form.TeachPass.set()
        else:
            await message.answer('На этом всё, регистрация окончена!', reply_markup=keyboard)
            await Form.Meny.set()

    if msg.lower() == 'нет':
        sql.execute(f"UPDATE users SET MAILING='{0}' WHERE ID={user_id}")
        db.commit()

        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Пары {str(NumGroup[0]).upper()}')
            btn1 = types.KeyboardButton(text=f'Пары на неделю {str(NumGroup[0]).upper()}')
            btn2 = types.KeyboardButton(text=f'Помощь/FAQ')
            keyboard.add(btn, btn1, btn2)

        await message.answer('На этом всё, регистрация окончена!', reply_markup=keyboard)
        await Form.Meny.set()


@dp.message_handler(state=Form.Meny)
async def SetMailing(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    
    for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
        category = category[0]
        
    if (len(msg.lower().split(' ')) == 2) and (msg.lower().split(' ')[0] == 'пары') or (len(msg.lower().split(' ')) == 3) and (msg.lower().split(' ')[0] == 'пары'):
        await message.answer('пары на 2 дня')

    if (len(msg.lower().split(' ')) == 4) and (msg.lower().split(' ')[1] == 'на') or (len(msg.lower().split(' ')) == 5) and (msg.lower().split(' ')[0] == 'пары'):
        await message.answer('пары на на неделю')

    if (msg.lower() == 'помощь/faq') and (category == 'студент'):
        await message.answer('текст помощи для студентов')

    if (msg.lower() == 'помощь/faq') and (category == 'преподаватель'):
        await message.answer('текст помощи для преподавателей')

    if msg.lower() == 'контактная информация':
        await message.answer('Текст контактной информации')

    if msg.lower() == 'режим работы':
        await message.answer('Режима работы')

    if (len(msg.lower().split(' ')) == 3) and (msg.lower().split(' ')[0] == 'учебный'):
        await message.answer('Файл с учебным планом для вашей группы')

    if msg.lower() == 'заявления':
        markup = types.InlineKeyboardMarkup(row_width=True)
        lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://drive.google.com/drive/folders/1b2_NXe9H0sVfdrpjKxt8JAjfdylWVwsL?usp=drive_link') 
        markup.add(lk1)
        await message.answer('вот ваши заявления', reply_markup=markup)

    if msg.lower() == 'заметка':
        if str(category).lower() == 'преподаватель':
            await message.answer('Заполните по данному примеру')
            await Form.AddNote.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

    if msg.lower() == 'сообщение':
        if str(category).lower() == 'преподаватель':
            await message.answer('Заполните по данному примеру')
            await Form.notification.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

    if (len(msg.lower().split(' ')) == 2) and (msg.lower().split(' ')[0] == 'заметка'):
        pass



@dp.message_handler(state=Form.AddNote)
async def AddNote(message: types.Message):
    pass

@dp.message_handler(state=Form.notification)
async def AddNote(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    msg = message.text

    for category in sql.execute(f"SELECT CATEGORY FROM users WHERE ID={user_id}"):
        category = category[0]

    if str(category) == 'преподаватель':
        for NumGroup in sql.execute(f"SELECT NUMGROUP FROM users WHERE ID={user_id}"):
            FullName = NumGroup[0]

        content = msg.split('\n')
        if content[0].lower() == 'внимание':
                content.pop(0)
                msg = ''.join(content)
                for i in sql.execute(f"SELECT ID FROM users WHERE MAILING={1}"):
                    print(i[0])
                    await bot.send_message(i[0], f"<a href='https://t.me/{username}'>{FullName}</a>\n{msg}", parse_mode=ParseMode.HTML)

        else:
            content.pop(0)
            msg = ''.join(content)
            
            for UserID in sql.execute(f"SELECT ID FROM users WHERE NUMGROUP='{content[0].lower()}' AND MAILING = {1}"): 
                await bot.send_message(UserID[0], f"<a href='https://t.me/{username}'>{FullName}</a>\n{msg}", parse_mode=ParseMode.HTML)
       
    else:
        await message.answer('У вас нет доступа к этой функции')

    await Form.Meny.set()



if __name__ =='__main__':
    executor.start_polling(dp)