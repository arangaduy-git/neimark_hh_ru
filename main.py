import asyncio
import logging
import random
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import CONST
import inline_fix_text
import kb
import sqlite3
import link
import parsing

TOKEN = CONST.BOT_TOKEN
dp = Dispatcher(storage=MemoryStorage())
times_list = ['part_time', 'from_4_hours', 'in_evening', "on_weekends"]
specialization_list = ['security', 'service_personnel', 'information_technology', 'mass_media', 'medicine', 'workers',
                       'retail', 'fitness', 'not_decided']
industry_list = ['car', 'hotels', 'JKH', 'internet', 'medicine1', 'social', 'food', 'components', 'retail1', 'building',
                 'non-food', 'computers', 'non_decided']
experience_list = ['doesnt_matter', '0', '1-3', '3-6', '6+']
disability_list = ['yes', 'no']
region_list = ['moscow', 'moscow_region', 'petersburg', 'leningrad', 'sevastopol', 'krasnodar', 'tatarstan',
               'nizhny_novgorod', 'yaroslavl']


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE userid = ?', (message.from_user.id,))
    results = cursor.fetchall()

    connection.close()

    if not results:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Users '
                       '(userid, name, region, time, specialization, industry, experience, disability)'
                       ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (message.from_user.id, '-1', '-1', -1, -1, -1, -1, -1))
        connection.commit()
        connection.close()
        path = f'images/start/{random.randint(1, 3)}.png'
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=FSInputFile(path=path),
                             caption='<b>Привет!</b> 🚀 \n\nЯ <b>Космиша</b>, и да, я прилетел из космоса, '
                                     'чтобы <b>помочь</b> тебе с поиском классной <b>подработки</b> 🌌. '
                                     'Я тут, чтобы сделать поиск подработки лёгким и даже весёлым! 😎'
                                     'Вместе мы найдём вариант, чтобы ты мог(ла) и зарабатывать, и '
                                     'получать удовольствие от жизни студента 🌟. Кстати, как к тебе '
                                     'обращаться? \n\n<b>Напиши</b> своё <b>ИМЯ и ФАМИЛИЮ</b>, и мы сразу начнем наш '
                                     'космический путь к подработке!', parse_mode='HTML')
    else:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE Users SET name = ?, region = ?, time = ?, specialization = ?, industry = ?, experience = ?, disability = ? WHERE userid = ?',
            ('-1', '-1', -1, -1, -1, -1, -1, message.from_user.id))
        connection.commit()
        connection.close()
        path = f'images/start/{random.randint(1, 3)}.png'
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=FSInputFile(path=path),
                             caption='<b>Привет!</b> 🚀 \n\nЯ <b>Космиша</b>, и да, я прилетел из космоса, '
                                     'чтобы <b>помочь</b> тебе с поиском классной <b>подработки</b> 🌌. '
                                     'Я тут, чтобы сделать поиск подработки лёгким и даже весёлым! 😎'
                                     'Вместе мы найдём вариант, чтобы ты мог(ла) и зарабатывать, и '
                                     'получать удовольствие от жизни студента 🌟. Кстати, как к тебе '
                                     'обращаться? \n\n<b>Напиши</b> своё <b>ИМЯ и ФАМИЛИЮ</b>, и мы сразу начнем наш '
                                     'космический путь к подработке!', parse_mode='HTML')


@dp.message()
async def echo_handler(message: Message, state: FSMContext) -> None:
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE userid = ?', (message.from_user.id,))
        results = cursor.fetchall()
        cursor.execute('SELECT name FROM Users WHERE userid = ?', (message.from_user.id,))
        name = cursor.fetchone()
        connection.close()

        if results[0][2] == '-1':
            if len(message.text.split()) == 2 and len(message.text) < 60:
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE Users SET name = ? WHERE userid = ?', (message.text, message.from_user.id))
                connection.commit()
                connection.close()
                path = f'images/region/{random.randint(1, 3)}.png'
                msg = await bot.send_photo(chat_id=message.from_user.id,
                                           photo=FSInputFile(path=path),
                                           caption=f'Приятно познакомиться, {message.text}! 🌟\n\n'
                                                   'Чтобы я мог подобрать наиболее удобные варианты '
                                                   'подработки специально для тебя, напомни, <b>в каком '
                                                   'РЕГИОНЕ/ГОРОДЕ ты живёшь?</b>\n\n🌆 Это поможет мне найти подработки, '
                                                   'которые будут не только интересны, но и удобны по местоположению.'
                                           , reply_markup=kb.region(), parse_mode='HTML')
                await state.update_data(chat_id=msg.chat.id)
                await state.update_data(message_id=msg.message_id)
            else:
                await message.answer('Укажите Имя и Фамилию')
        else:
            await message.answer('Выполните шаг выше!')
    except TypeError:
        await message.answer("Nice try!")


@dp.callback_query(lambda F: F.data in region_list)
async def region(callback: CallbackQuery, state: FSMContext):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET region = ? WHERE userid = ?',
                   (callback.data, callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    path = f'images/time/{random.randint(1, 3)}.png'
    msg = await bot.send_photo(chat_id=callback.from_user.id,
                               photo=FSInputFile(path=path),
                               caption=f'Прекрасно, {name[0]}! 🚀\n\nЯ готов помочь тебе найти подработку, '
                                       'которая идеально впишется в твой график 🌠. Ведь кто сказал, что нельзя '
                                       'зарабатывать и оставаться свободным, как комета в открытом космосе? \n\n'
                                       '🌌<b>Выбери ВРЕМЯ, когда тебе удобно работать</b>, и мы продолжим наш '
                                       'межгалактический поиск подходящей подработки!'
                               , reply_markup=kb.main(), parse_mode='HTML')
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f'Приятно познакомиться, {name[0]}! 🌟\n\n'
                                                    'Чтобы я мог подобрать наиболее удобные варианты '
                                                    'подработки специально для тебя, напомни, <b>в каком '
                                                    'РЕГИОНЕ/ГОРОДЕ ты живёшь?</b>\n\n🌆 Это поможет мне найти подработки, '
                                                    'которые будут не только интересны, но и удобны по местоположению.\n\n'
                                                    f'Ты выбрал - <b>{inline_fix_text.region_kb_list[callback.data]}</b>')
    await state.update_data(chat_id=msg.chat.id)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data in times_list)
async def time(callback: CallbackQuery, state: FSMContext):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET time = ? WHERE userid = ?',
                   (times_list.index(callback.data), callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    path = f'images/specialization/{random.randint(1, 3)}.png'
    msg = await bot.send_photo(chat_id=callback.from_user.id,
                               photo=FSInputFile(path=path),
                               caption=f"Отличный выбор, {name[0]}! 🌟\n\nТы на правильном пути к тому, "
                                       "чтобы найти подработку, которая принесет тебе не только доход, но и радость! 😄\n\n"
                                       "<b>Выбери</b> свою <b>СПЕЦИАЛИЗАЦИЮ</b>, и мы продолжим наш захватывающий космический "
                                       "путь к идеальной подработке! 🌌", reply_markup=kb.specialization(),
                               parse_mode='HTML')
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f'Прекрасно, {name[0]}! 🚀\n\nЯ готов помочь тебе найти подработку, '
                                                    'которая идеально впишется в твой график 🌠. Ведь кто сказал, что нельзя '
                                                    'зарабатывать и оставаться свободным, как комета в открытом космосе?\n\n'
                                                    '🌌<b>Выбери ВРЕМЯ,когда тебе удобно работать</b>, и мы продолжим наш '
                                                    'межгалактический поиск подходящей подработки!\n\n'
                                                    f'Ты выбрал - <b>{inline_fix_text.main_kb_list[callback.data]}</b>')
    await state.update_data(chat_id=msg.chat.id)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data in specialization_list)
async def specialization(callback: CallbackQuery, state: FSMContext):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET specialization = ? WHERE userid = ?',
                   (specialization_list.index(callback.data), callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    path = f'images/industry/{random.randint(1, 3)}.png'
    msg = await bot.send_photo(chat_id=callback.from_user.id,
                               photo=FSInputFile(path=path),
                               caption=f"Хорошо, {name[0]}! 😎\n\nТы точно знаешь, чего хочешь! Теперь давай "
                                       "определимся с <b>ОТРАСЛЬЮ компании</b>, в которой тебе хотелось бы работать. "
                                       "Это поможет сузить поиск и найти подходящую подработку! 🌌\n\n"
                                       "Выбери нужную отрасль, и мы будем на шаг ближе к идеальной подработке для тебя! 🚀",
                               reply_markup=kb.industry(), parse_mode='HTML')
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f"Отличный выбор, {name[0]}! 🌟\n\nТы на правильном пути к тому, "
                                                    "чтобы найти подработку, которая принесет тебе не только доход, но и радость! 😄 \n"
                                                    "<b>Выбери</b> свою <b>СПЕЦИАЛИЗАЦИЮ</b>, и мы продолжим наш захватывающий космический "
                                                    "путь к идеальной подработке! 🌌\n\n"
                                                    f'Ты выбрал - <b>{inline_fix_text.specialization_kb_list[callback.data]}</b>')
    await state.update_data(chat_id=msg.chat.id)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data in industry_list)
async def industry(callback: CallbackQuery, state: FSMContext):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET industry = ? WHERE userid = ?',
                   (industry_list.index(callback.data), callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    path = f'images/experience/{random.randint(1, 3)}.png'
    msg = await bot.send_photo(chat_id=callback.from_user.id,
                               photo=FSInputFile(path=path),
                               caption=f"Прекрасный выбор, {name[0]}! 🏆\n\nТы уже почти у цели! "
                                       "Осталось несколько важных шагов. Расскажи, есть ли у тебя <b>ОПЫТ работы</b> в "
                                       "данной сфере.\n\nЭто поможет мне подобрать вакансии, которые максимально "
                                       "соответствуют твоему уровню подготовки! 🌌✨"
                                       "Выбери подходящий вариант, и я подберу для тебя лучшие предложения! 🚀",
                               reply_markup=kb.experience(), parse_mode='HTML')
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f"Хорошо, {name[0]}! 😎\n\nТы точно знаешь, чего хочешь! Теперь давай "
                                                    "определимся с <b>ОТРАСЛЬЮ компании</b>, в которой тебе хотелось бы работать. "
                                                    "Это поможет сузить поиск и найти подходящую подработку! 🌌\n\n"
                                                    "Выбери нужную отрасль, и мы будем на шаг ближе к идеальной подработке для тебя! 🚀\n\n"
                                                    f'Ты выбрал - <b>{inline_fix_text.industry_kb_list[callback.data]}</b>')
    await state.update_data(chat_id=msg.chat.id)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data in experience_list)
async def experience(callback: CallbackQuery, state: FSMContext):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET experience = ? WHERE userid = ?',
                   (experience_list.index(callback.data), callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    path = f'images/disability/{random.randint(1, 3)}.png'
    msg = await bot.send_photo(chat_id=callback.from_user.id,
                               photo=FSInputFile(path=path),
                               caption=f"Замечательный выбор, {name[0]}! 🌈\n\nМы уже близки к тому, чтобы найти "
                                       "для тебя отличные предложения! У меня остался последний вопрос к тебе. "
                                       "Не подскажешь, являешься ли ты человеком с <b>ограниченными возможностями</b>?\n\n"
                                       "Это поможет мне учесть все важные детали при поиске подходящих вакансий. 💖 "
                                       "Спасибо, что делишься этой информацией! 🚀", reply_markup=kb.disability())
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f"Прекрасный выбор, {name[0]}! 🏆\n\nТы уже почти у цели! "
                                                    "Осталось несколько важных шагов. Расскажи, есть ли у тебя <b>ОПЫТ работы</b> в "
                                                    "данной сфере.\n\nЭто поможет мне подобрать вакансии, которые максимально "
                                                    "соответствуют твоему уровню подготовки! 🌌✨"
                                                    "Выбери подходящий вариант, и я подберу для тебя лучшие предложения! 🚀\n\n"
                                                    f'Ты выбрал - <b>{inline_fix_text.experience_kb_list[callback.data]}</b>')
    await state.update_data(chat_id=msg.chat.id)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(lambda F: F.data in disability_list)
async def disability(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Одну минутку, анализирую ваши данные!')
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET disability = ? WHERE userid = ?',
                   (disability_list.index(callback.data), callback.from_user.id))
    connection.commit()
    cursor.execute('SELECT name FROM Users WHERE userid = ?', (callback.from_user.id,))
    name = cursor.fetchone()
    connection.close()
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await callback.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, reply_markup=None,
                                            caption=f"Замечательный выбор, {name[0]}! 🌈\n\nМы уже близки к тому, чтобы найти "
                                                    "для тебя отличные предложения! У меня остался последний вопрос к тебе. "
                                                    "Не подскажешь,  являешься ли ты человеком с <b>ограниченными возможностями</b>?\n\n"
                                                    "Это поможет мне учесть все важные детали при поиске подходящих вакансий. 💖 "
                                                    "Спасибо, что делишься этой информацией!\n\n"
                                                    f'Ты выбрал - <b>{inline_fix_text.disability_kb_list[callback.data]}</b>')
    link_vac = link.get_link(callback.from_user.id)
    print(link_vac)
    vacs = parsing.get_vacs(link_vac)
    if not vacs:
        await bot.send_message(chat_id=callback.from_user.id, text='Увы, <b>подработки для вас не нашлось</b>.\n\nПопробуйте выбрать <b>другую специализацию или отрасль</b>, для этого напишите /start',
                               parse_mode='HTML')
    else:
        path = f'images/last_msg/{random.randint(1, 3)}.png'
        text = f'Отлично, {name[0]}! 🎉\n\nЯ нашёл несколько интересных <b>подработок</b>, которые могут тебе подойти. Вот три варианта: \n'
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=FSInputFile(path=path),
                             caption=text, reply_markup=None, parse_mode='HTML')
        for i in range(len(vacs)):
            text = (f'<b>💻 Работа {i + 1}:</b> {vacs[i][0]}\n'
                    f'<b>📍 Локация:</b> {vacs[i][4]}\n'
                    f'<b>💵 Зарплата:</b> {vacs[i][1]}\n'
                    f'<b>⭐️ Опыт:</b> {vacs[i][2]}\n'
                    f'<b>💼 Работадатель:</b> {vacs[i][3]}.\n'
                    f'<b>🔗 Ссылка:</b> <a href="{vacs[i][5]}">Клик</a>\n')
            await bot.send_message(chat_id=callback.from_user.id, text=text, parse_mode='HTML')
        text = f'Если ты хочешь <b>посмотреть все доступные варианты</b>, вот общий лист подработок: <a href="{link_vac}">Клик</a>\n\nА если хочешь <b>начать сначала</b>, напиши /start'
        await bot.send_message(chat_id=callback.from_user.id, text=text, parse_mode='HTML')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    name TEXT,
    region TEXT,
    time INTEGER,
    specialization INTEGER,
    industry INTEGER,
    experience INTEGER,
    disability BOOL
    )
    ''')
    connection.commit()
    connection.close()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
