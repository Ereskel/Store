# в начале должна быть прописана кодировка.
# -*- coding: utf-8 -*import
import random

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from loader import dp, Bot, router1, bot
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram import types, Router
from captcha.image import ImageCaptcha
from random import choice
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import FSInputFile
from db import add_user, create_database, get_user, admin_add_staff, create_database_staff
from state import Start, Add_staff, Staff, Staff2
from config import admins, moder_id

from keyboards.default import kb, admin_kb, admin2_kb
from keyboards.inline import inline_kb, generate_city, generate_area, inline_kb3

'''
Кнопка СТАРТ! При нажатии происходит генерация капчи. Если пользователь уже есть в базе, ничего не происходит. Если по-
льзователя нет, то происходит генерация капчи. После её прохождения капча не выводится. Важный момент - пользователь 
сразу попадает в базу данных, независимо от того прошел он капчу, или нет. 

Модернизация. Для последующей модернизации необходимо создать дополнительную графу прошел чел капчу или нет. Ну и соотве
тственно значение установить дефолтное в ноль, а при прохождении в единицу. Если гет captcha будет == 1, то гуд. Если нет
даем ему капчу и проверяем прошел он её или нет. Если прошел, значит инсерт в графу единичку.

Вопрос актуален по принципу занесения шопа на ветрину. Так и не понятно каким образом осуществить пересылку. Проблема заключается не в 
самой пересылке сообщения, а в передачи данных из стейта. Данные занесенные пользователем в стейт, доступны только по его chat_id и 
(что важно) сохраняются только в его чате. То есть пересылка дает гипотетическую возможность узнать chat.id пользователя и все данные
сохраненные в стейте. Но все эти данные не пригодны для последующего использования где либо. То есть их нужно вычленять непосредственно из сообщения.
Вопрос заключается в том, как это сделать. Конкретно здесь, хотелось бы узнать как мне вытащить chat.id. Чат гпт накинул интересную идею кстати.
Он предложил разделить две таблицы базы данных. Создать таблицу отмодерированных магазов и тех, которые только только должны пройти модерацию. 
Это решает ряд задач. Но остается вопрос удобства и автоматики. Заносить данные в базу данных можно и вручную. Но это совершенно несовершенно.
А ну кстате вообщето это ахуенно все упрощает. По сути задача будет состоять в переносе данных из одной таблицы в другую. И это можно сделать 
при нажатии на одну клавишу. Ну все тогда. Будем нахуй пробовать.

Ебать охуенно гениальная идея кстати! Я почему то об этом блять не подумал ваще. Это внатуре гениально
inline_res = InlineKeyboardButton('Рассчитать', callback_data='asdf {message.text}')
'''


@router1.message(Command('start'))
async def handler1(message: Message):
    await create_database_staff()
    id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    image = ImageCaptcha(fonts=['caviar-dreams.ttf'], width=300, height=150)
    letters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'Q', 'q', 'H', 'h', 'I', 'i',
               'J', 'j', 'K', 'k', 'L', 'l' 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'R', 'r',
               '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    code = []
    for i in range(7):
        code.append(choice(letters))
    image.write(code, 'out.png')
    photo = FSInputFile('out.png')
    a = ''
    for el in code:
        a += str(el)
    print(a)
    print(code)
    if await get_user(id) is None:
        await add_user(id, name, username)
        await SendPhoto(chat_id=message.from_user.id, photo=photo)
    else:
        await message.answer('Вы уже в команде. Для вас действуют уникальные условия!', reply_markup=kb)

    @router1.message(Text(a))
    async def handler2(message: Message):
        await message.answer('Добро пожаловать на борт!')
    # else:
    # /   await message.answer('Вы уже есть в базе. Для вас уникальные условия!')


@router1.message(Text('🛒 Купить товары 🛒'))
async def handler3(message: types.Message, state: FSMContext):
    inline_kb2, data = await generate_city()
    await message.answer('Выберите интересующий вас товар', reply_markup=inline_kb2)
    await state.set_state(Staff.state1)


@router1.callback_query(Staff.state1)
async def handler10(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    inline_kb3 = await generate_area()
    if callback.data == "Крекшино":
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_kb3)
    #            await state.set_state(Staff2.state1)   
    await callback.message.answer('Привет')


@router1.message(Command('admin'))
async def get_admin(message: Message, state: FSMContext):
    id = message.from_user.id
    if admins == id:
        await message.answer('Приветствую тебя админ. Ты просто бомба.', reply_markup=admin_kb)
        await state.set_state(Add_staff.state1)
    else:
        pass


@router1.message(Text('Зарегестрировать свой магазин'))
async def handler4(message: Message, state: FSMContext):
    await message.answer('Введите название продукта')
    await state.set_state(Add_staff.state1)


@router1.message(Add_staff.state1)
async def handler5(message: Message, state: FSMContext):
    await message.answer('Введите ваш населенный пункт (место где осуществляется продажа товара)')
    await state.update_data(name=message.text)
    await state.set_state(Add_staff.state2)


@router1.message(Add_staff.state2)
async def handler5(message: Message, state: FSMContext):
    await message.answer('Введите стоимость товара.')
    await state.update_data(city=message.text)
    await state.set_state(Add_staff.state3)


@router1.message(Add_staff.state3)
async def handler6(message: Message, state: FSMContext):
    await message.answer('Введите описание товара (подчеркните некоторые особенности, которые будут вашим преимуществом'
                         'на фоне конкурентов, а также напишите количество товара в наличие.)')
    await state.update_data(amount=message.text)
    await state.set_state(Add_staff.state4)


@router1.message(Add_staff.state4)
async def handler21(message: Message, state: FSMContext):
    await message.answer('Введите контактную информацию (любые контактные данные. Это может быть номер телефона, почта'
                         'и т.д.')
    await state.update_data(description=message.text)
    await state.set_state(Add_staff.state5)


@router1.message(Add_staff.state5)
async def handler21(message: Message, state: FSMContext):
    await message.answer('Отправьте фотографию товара. Если нет желания её добавлять просто нажмите кнопку пропустить')
    await state.update_data(info=message.text)
    await state.set_state(Add_staff.state6)


@router1.message(Add_staff.state6)
async def handler7(message: Message, state: FSMContext):
    chat_id = message.chat.id
    photo_id = message.photo[-1].file_id
    print(f'Photo id: {photo_id}')
    await state.update_data(photo=photo_id)
    data = await state.get_data()
    name = data.get('name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    caption = f'Проверьте введенные данные:\n\n'\
              f'Наименование товара - {name} \n'\
              f'Город - {city} \n'\
              f'Стоимость - {amount}\n'\
              f'Описание товара - {description}\n'\
              f'Информация о продавце - {info}\n'\
              #f'Фото - {photo}'
    await bot.send_photo(chat_id=chat_id, photo=photo_id, caption = caption, reply_markup=admin2_kb)
    await state.set_state(Add_staff.state7)


@router1.message(Text('Подтвердить ввод'), Add_staff.state7)
async def handler8(message: Message, state: FSMContext):
    await message.answer('Заявка ожидает модерации. Обычно это занимает несколько минут')
    data = await state.get_data()
    name = data.get('name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    photo_id = data.get('photo')
    caption = f'Проверьте введенные данные:\n\n' \
              f'Наименование товара - {name} \n' \
              f'Город - {city} \n' \
              f'Стоимость - {amount}\n' \
              f'Описание товара - {description}\n' \
              f'Информация о продавце - {info}\n' \
        # f'Фото - {photo}'\
    await bot.send_photo(chat_id = moder_id, photo = photo_id, caption = caption, reply_markup = inline_kb3)
    await state.set_state(Add_staff.state8)


@router1.callback_query(Text('add_shop'), Add_staff.state8)
async def handler89(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    photo_id = data.get('photo')
    await admin_add_staff(None, name, city, amount, description, info, photo_id)




@router1.message(Add_staff.state8)
async def handler88(message: Message, state: FSMContext):
    await message.answer('Заявка отправлена на модерацию. Ответ придет в течении пяти дней. ')
    data = await state.get_data()
    name = data.get('name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    photo = data.get('photo')
#    await bot.send_message(chat_id = moder_id, text = text_message)

# @router1.message(Command('start'))
# async def handler_1(message: types.Message, state: FSMContext) -> None:
#    id = message.from_user.id
#    name = message.from_user.first_name
#    username = message.from_user.username
#    user_exists = await get_user(id)

#    if user_exists:
#        # Если пользователь уже есть в базе, отправляем приветственное сообщение
#        await message.answer('Элитный спецназ вас приветствует!')
#    else:
#        # Если пользователя нет в базе, генерируем новую капчу и отправляем её ему
#        image = ImageCaptcha(fonts=['caviar-dreams.ttf'], width=300, height=150)
#        letters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'Q', 'q', 'H', 'h', 'I', 'i',
#                   'J', 'j', 'K', 'k', 'L', 'l' 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'R', 'r',
#                   '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
#        code = []
#        for i in range(7):
#            code.append(choice(letters))
#        image.write(code, 'out.png')
#        photo = FSInputFile('out.png')
#        a = ''
#        for el in code:
#            a += str(el)
#        print(a)
#        await SendPhoto(chat_id=message.from_user.id, photo=photo)
#        print(code)

# Устанавливаем состояние пользователя в Start, чтобы сохранить в нём код капчи
#        await state.set_state(Start.captcha_check)
#        await state.update_data(captcha=a, id=id, name=name, username=username)


# @router1.message(Start.captcha_check)
# async def captcha_check(message: Message, state: FSMContext):
#    data = await state.get_data()
#    captcha = data['captcha']
#    user_id = data['id']
#    name = data['name']
#    username = data['username']

#    if message.text == captcha:
# Если капча решена правильно, добавляем пользователя в базу данных
#        await add_user(user_id, name, username)
#        await state.finish()
#        await message.answer('Капча решена верно! Добро пожаловать в наш бот!')
