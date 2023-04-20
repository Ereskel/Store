# в начале должна быть прописана кодировка.
# -*- coding: utf-8 -*import
import random

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from loader import dp, Bot, router1
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram import types, Router
from captcha.image import ImageCaptcha
from random import choice
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import FSInputFile
from db import add_user, create_database, get_user, admin_add_staff, create_database_staff
from state import Start, Add_staff
from config import admins


from keyboards.default import kb, admin_kb, admin2_kb
from keyboards.inline import inline_kb, generate

@router1.message(Command('start'))
async def handler1(message: Message):
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

async def handler44(callback: types.CallbackQuery):
    await generate()
    data = callback.data
    return data


@router1.message(Text('Кнопка 1'))
async def handler3(message: types.Message):
    inline_kb2 = await generate()
    await handler44()
    await message.answer('Выберите нужную вам категорию', reply_markup=inline_kb2)



        @router1.callback_query(Text(data))
        async def handler10(callback: types.CallbackQuery):
            await callback.message.answer('Привет')


@router1.message(Command('admin'))
async def get_admin(message: Message, state: FSMContext):
    id = message.from_user.id
    if admins == id:
        await message.answer('Приветствую тебя админ. Ты просто бомба.', reply_markup=admin_kb)
        await state.set_state(Add_staff.state1)
    else:
        pass


@router1.message(Text('Кнопка 6'), Add_staff.state1)
async def handler4(message: Message, state: FSMContext):
    await message.answer('Введи нужный город')
    await state.set_state(Add_staff.state2)


@router1.message(Add_staff.state2)
async def handler5(message: Message, state: FSMContext):
    await message.answer('Введите район')
    await state.update_data(city=message.text)
    await state.set_state(Add_staff.state3)

@router1.message(Add_staff.state3)
async def handler6(message: Message, state: FSMContext):
    await message.answer('Введите товар')
    await state.update_data(area=message.text)
    await state.set_state(Add_staff.state4)

@router1.message(Add_staff.state4)
async def handler7(message: Message, state: FSMContext):
    await state.update_data(staff=message.text)
    data = await state.get_data()
    city = data.get('city')
    area = data.get('area')
    staff = data.get('staff')
    await message.answer(f'Проверьте введенные данные:\n\n'
                         f'Город - {city} \n'
                         f'Район - {area} \n'
                         f'Товар - {staff}', reply_markup=admin2_kb)
    await state.set_state(Add_staff.state5)

@router1.message(Text('Подтвердить ввод'),Add_staff.state5)
async def handler8(message: Message, state: FSMContext):
    await message.answer('Че еще хочешь типок бля')
    data = await state.get_data()
    city = data.get('city')
    area = data.get('area')
    staff = data.get('staff')
    await admin_add_staff(city, area, staff)

@router1.message(Text(''))
