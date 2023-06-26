from aiogram import types, Router
from captcha.image import ImageCaptcha
from random import choice
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import FSInputFile
from db import add_user, create_database, get_user, admin_add_staff, create_database_staff, delete_staff, \
    get_data_staff, create_database_staff2, admin_add_staff_valid, get_data_staff_valid
from state import Start, Add_staff, Staff, Staff2
from config import admins, moder_id

from keyboards.default import kb, admin_kb, admin2_kb
from keyboards.inline import inline_kb, generate_city, generate_area, inline_kb3, generate_add

'''
Кнопка СТАРТ! При нажатии происходит генерация капчи. Если пользователь уже есть в базе, пасуем. После её прохождения капча не выводится. Важный момент - пользователь 
сразу попадает в базу данных, независимо от того прошел он капчу, или нет. 

Модернизация. Для последующей модернизации необходимо создать дополнительную графу прошел чел капчу или нет. Ну и соответственно 
значение установить дефолтное в ноль, а при прохождении в единицу. Если гет captcha будет == 1, то гуд. Если нет
даем ему капчу и проверяем прошел он её или нет. Если прошел, значит инсерт в графу единичку.
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
        await message.answer('Приветствую тебя админ..', reply_markup=admin_kb)
        await state.set_state(Add_staff.state1)
    else:
        pass


@router1.message(Text('Зарегестрировать свой магазин'))
async def handler4(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db_data = await get_data_staff(user_id)
    db_data_valid = await get_data_staff_valid(user_id)
    print(db_data)
    if db_data:
        await message.answer('Ваша заявка находится на рассмотрении.')
    if db_data_valid:
        await message.answer('У вас уже есть зарегестрированный магазин.4')
    else:
        await message.answer('Введите название продукта')
        await state.set_state(Add_staff.state1)


@router1.message(Add_staff.state1)
async def handler5(message: Message, state: FSMContext):
    await message.answer('Введите ваш населенный пункт (место где осуществляется продажа товара)')
    await state.update_data(shop_name=message.text)
    await state.set_state(Add_staff.state2)


@router1.message(Add_staff.state2)
async def handler5(message: Message, state: FSMContext):
    await message.answer('Введите стоимость товара.')
    await state.update_data(city=message.text)
    await state.set_state(Add_staff.state3)


@router1.message(Add_staff.state3)
async def handler6(message: Message, state: FSMContext):
    await message.answer('Введите описание товара (подчеркните некоторые особенности, которые будут вашим преимуществом'
                         'на фоне конкурентов, а также напишите количество товара в наличии.)')
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
    shop_name = data.get('shop_name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    caption = f'Проверьте введенные данные:\n\n' \
              f'Наименование товара - {shop_name} \n' \
              f'Город - {city} \n' \
              f'Стоимость - {amount}\n' \
              f'Описание товара - {description}\n' \
              f'Информация о продавце - {info}\n' \
        # f'Фото - {photo}'
    await create_database_staff2()
    await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption, reply_markup=admin2_kb)
    await state.set_state(Add_staff.state7)


@router1.message(Text('Подтвердить ввод'), Add_staff.state7)
async def handler8(message: Message, state: FSMContext):
    await message.answer('Заявка ожидает модерации. Обычно это занимает несколько минут')
    user_id = message.from_user.id
    print(user_id)
    username = message.from_user.username
    name = message.from_user.first_name
    await state.update_data(user_id = user_id)
    data = await state.get_data()
    shop_name = data.get('shop_name')
    city = data.get('city')
    amount = data.get('amount')
    description = data.get('description')
    info = data.get('info')
    photo_id = data.get('photo')
    await admin_add_staff(None, user_id, name, username, shop_name, city, amount, description, info, photo_id)
    # Вот здесь мы осуществляем добавление данных в базу. От этого надо плясать. И теперь данные мы будем
    # забирать из базы а не из стейтов/
    # Проверяем занеслись ли данные на сервак.
    await get_data_staff(user_id)
    db_data = await get_data_staff(user_id)
    print(db_data)
    db_user_id = db_data[1]
    db_name = db_data[2]
    db_username = db_data[3]
    db_shop_name = db_data[4]
    db_city = db_data[5]
    db_amount = db_data[6]
    db_description = db_data[7]
    db_info = db_data[8]
    db_photo_id = db_data[9]
    caption = f'Новая заявка от пользователя: {db_user_id}\n\n' \
              f'Проверьте введенные данные:\n\n' \
              f'Наименование товара - {db_shop_name} \n' \
              f'Город - {db_city} \n' \
              f'Стоимость - {db_amount}\n' \
              f'Описание товара - {db_description}\n' \
              f'Информация о продавце - {db_info}\n' \
        # f'Фото - {photo}'\
    inline_kb_6 = await generate_add(user_id)
    await bot.send_photo(chat_id=1405036352, photo=photo_id, caption=caption, reply_markup=inline_kb_6)
    #  await bot.send_photo(chat_id=1405036352, photo=photo_id, caption=caption, reply_markup=inline_kb3)
    await state.clear()


@router1.callback_query()
async def handler9(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data
    print(callback_data)
    if callback_data[0] == 'add_shop':
        user_id = callback_data[1]
        await callback.message.answer(f'Вы выбрали добавление пользователя с идентификатором {user_id}')
    elif callback_data[0] == 'decline_user':
        await callback.message.answer('Заявка отклонена')
#    await get_data_staff(user_id)
 #   await admin_add_staff_valid(None, user_id, name, username, shop_name, city, amount, description, info, photo_id)


@router1.callback_query(Text('decline_shop'), Add_staff.state8)
async def handler90(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Приветик!)')

    print(user_id)
    data = await state.get_data()
 #   user_id =
  #  print(user_id)
   # await delete_staff(user_id)


#@router1.message(Add_staff.state8)
#async def handler88(message: Message, state: FSMContext):
#    await message.answer('Заявка отправлена на модерацию. Ответ придет в течении пяти дней. ')
#    data = await state.get_data()
#    name = data.get('name')
#    city = data.get('city')
#    amount = data.get('amount')
#    description = data.get('description')
#    info = data.get('info')
#fdfd    photo = data.get('photo')
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
